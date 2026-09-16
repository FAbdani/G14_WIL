# Import the tools needed for recording and speech recognition
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import subprocess
from datetime import datetime
from pathlib import Path
from difflib import SequenceMatcher
import pandas as pd


# Find the main GitHub project folder
project_folder = Path(__file__).resolve().parent

# Connect to the question and answer files from GitHub
questions_file = project_folder / "data" / "topics.csv"
answers_file = project_folder / "data" / "golden_summaries.csv"


# Load the GitHub questions and answers
questions_df = pd.read_csv(questions_file)
answers_df = pd.read_csv(answers_file)

# Join each question to its corresponding expected answer
question_answer_df = questions_df.merge(answers_df[["question_id", "summary"]],on="question_id")

print(len(question_answer_df),"questions and answers were loaded from GitHub.")


# The recording settings
sample_rate = 16000
recording_time = 10


# Tell the user what to do
print()
print("Recording for 10 seconds...")
print("Please say one of the questions from topics.csv.")


# Record audio from the laptop microphone
recording = sd.rec(
    int(recording_time * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="int16"
)

# Wait until the recording is finished
sd.wait()


# Create a different filename using the current date and time
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
audio_file = f"travel_question_{current_time}.wav"

# Save the recording as a WAV file
write(audio_file, sample_rate, recording)

print("Recording finished.")
print("The question is now being transcribed...")


# Load the base Whisper model
# The CPU and int8 settings allow it to run without a graphics card
model = WhisperModel("base",device="cpu",compute_type="int8")


# Transcribe the recorded question
segments, information = model.transcribe(audio_file,language="en",beam_size=5)


# Join the transcribed sections into one sentence
transcribed_text = ""

for segment in segments:
    transcribed_text += segment.text.strip() + " "

transcribed_text = transcribed_text.strip()


# Display the transcription
print("Detected language:", information.language)
print("Transcribed text:", transcribed_text)


# Continue only if speech was detected
if transcribed_text:

    best_row = None
    best_score = 0

    # Compare the transcription with every question from topics.csv
    for index, row in question_answer_df.iterrows():

        saved_question = str(row["question"])

        similarity_score = SequenceMatcher(
            None,
            transcribed_text.lower(),
            saved_question.lower()
        ).ratio()

        # Remember the most similar question
        if similarity_score > best_score:
            best_score = similarity_score
            best_row = row


    # Only provide an answer when the match is strong enough
    if best_row is not None and best_score >= 0.55:

        matched_question_id = best_row["question_id"]
        matched_question = best_row["question"]
        matched_answer = best_row["summary"]

        print()
        print("Matched question ID:", matched_question_id)
        print("Matched question:", matched_question)
        print("Match score:", round(best_score, 2))
        print("Answer:", matched_answer)
        print("Reading the answer aloud...")

        # Read the matched answer aloud
        subprocess.run([
            "edge-playback",
            "--text",
            str(matched_answer),
            "--voice",
            "en-AU-NatashaNeural"
        ])

    else:
        print()
        print("The question did not closely match a question in topics.csv.")

else:
    print("No speech was detected, so there is nothing to answer.")
