# Import the tools needed for recording and speech recognition
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import subprocess
from datetime import datetime

# Import the RAG function made by the team
from src.retrieval.rag_system import answer_question_with_sources


# Settings for the voice recording
sample_rate = 16000
recording_time = 10


# Let the user know that the recording is starting
print()
print("Recording for 10 seconds...")
print("Please ask a question about Australian visa information.")


# Record the user's voice through the microphone
recording = sd.rec(
    int(recording_time * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="int16"
)

# Wait until the full 10 seconds have been recorded
sd.wait()


# Add the current date and time to the audio filename
# This stops each new recording from replacing the previous one
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
audio_file = f"travel_question_{current_time}.wav"


# Save the recording as a WAV file
write(audio_file, sample_rate, recording)

print("Recording finished.")
print("The question is now being transcribed...")


# Load the base Whisper model
# I am using CPU and int8 because my laptop does not need a graphics card for this
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


# Use Whisper to convert the recorded voice into text
segments, information = model.transcribe(
    audio_file,
    language="en",
    beam_size=5
)


# Whisper may return the transcription in different sections
# This joins all of the sections into one complete question
transcribed_text = ""

for segment in segments:
    transcribed_text = transcribed_text + segment.text.strip() + " "

transcribed_text = transcribed_text.strip()


# Show what Whisper heard
print("Detected language:", information.language)
print("Transcribed question:", transcribed_text)


# Only search for an answer if some speech was detected
if transcribed_text:

    print()
    print("Searching for an answer...")

    try:
        # Send the transcribed question to the team's RAG system
        rag_result = answer_question_with_sources(transcribed_text)

        # The RAG system returns the answer and the sources it used
        answer = rag_result["answer"]
        sources = rag_result["sources"]

        print()
        print("Answer:", answer)


        # Show the source passage IDs if any sources were found
        if sources:

            print()
            print("Sources used:")

            for source in sources:
                passage_id = source["passage_id"]
                similarity = source["similarity"]

                print(
                    "- Passage:",
                    passage_id,
                    "| Similarity:",
                    round(similarity, 3)
                )


        # Read the generated answer aloud
        print()
        print("Reading the answer aloud...")

        # Use the same Python installation to run Edge playback
        # This avoids problems if edge-playback is not available through PATH
        subprocess.run([
            "edge_playback",
            "--text",
            answer,
            "--voice",
            "en-AU-NatashaNeural"
        ])

    # Display the error instead of stopping the whole program
    except Exception as error:
        print()
        print("The program could not generate an answer.")
        print("Error:", error)


# This happens if Whisper did not detect any speech
else:
    print("No speech was detected, so there is nothing to answer.")