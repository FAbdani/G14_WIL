# G14_WIL

## Team Assignments

| Name   | Student ID        |
|--------|--------------------|
| Fatima Abdani | s4100500 |
| Kashaf Fatima | s4104802  | 
| Darshana Gorantla | s4165839 |
| Jennie Lee | s4077970 |  
| Richy Naveenoa | s4178251  | 

## Run the app on Windows

Use **64-bit Python 3.14** and PowerShell. Run the commands below from the repository root after cloning. Other Python versions and operating systems have not been verified for this setup.

Create a separate app environment. This preserves any existing `.venv` used for research scripts:

```powershell
py -3.14 -m venv .venv-app
.\.venv-app\Scripts\python.exe -m pip install --only-binary=:all: -r requirements-app.txt
.\.venv-app\Scripts\python.exe -m pip check
```

Using the environment's Python directly means activation and PowerShell execution-policy changes are unnecessary. The binary-only option avoids attempting to compile unsupported native packages locally.

`requirements-app.txt` pins the app's direct dependencies, including speech recognition, speech playback, and translation. The original `requirements.txt` remains available for the team's older research/evaluation scripts; it is **not the app installation command** and should not be installed into `.venv-app`. It contains legacy pins that can fail on newer Python versions. Transitive dependencies are resolved by pip, so this is not a full lockfile.

Install the desktop service from [Ollama](https://ollama.com), open it, then download both answer-generation models:

```powershell
ollama pull llama3.2
ollama pull qwen2.5:3b-instruct
ollama list
```

Keep Ollama running and launch the website:

```powershell
.\.venv-app\Scripts\python.exe -m streamlit run app.py
```

Open the local address printed in the terminal. No interactive `ollama run` session or `/bye` command is needed to use the website.

On first use, the application downloads the multilingual models listed below and the Whisper `base` speech-recognition model. Allow several GB of free disk space and an internet connection. Models are cached for future runs; initial startup can be much slower. Speech playback uses the online Edge speech service, so that feature requires internet access and sends the answer text to that service.

## Verify the installation

```powershell
.\.venv-app\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

Then check the app in a browser:

1. Ask a typed travel-document question and open its supporting source.
2. Allow microphone access, record the same question, and check the recognised question and answer.
3. Play an answer using the speech control and confirm it is audible.
4. Ask a supported question in another supported language and check its response.
5. Clear the conversation and check that a new question works.

Automated tests alone do not verify browser microphone permissions or audible playback. See `docs/app_setup_validation.md` for the installation checks and remaining manual checks.

### Multilingual Prototype Setup

The multilingual prototype uses three local models:

- `BAAI/bge-m3` - multilingual retrieval (~2.2 GB)
- `qwen2.5:3b-instruct` - passage selection and grounded answer generation (1.9 GB)
- `facebook/nllb-200-distilled-600M` - multilingual translation (~2.5 GB)

Total first-time model download is approximately 6.5-7 GB.

#### 1. Install project dependencies

From the project root:

1. Install `requirements-app.txt` in `.venv-app` using the instructions above.

2. Download qwen2.5 : run 'ollama pull qwen2.5:3b-instruct'

3. Launch the app. BGE-M3 and NLLB are downloaded automatically from Hugging Face when the multilingual module first loads.

**The downloaded models are cached locally and do not need to be downloaded again for later runs.**
