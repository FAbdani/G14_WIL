# App installation validation

Date: 26 September 2026. Branch: `fix-app-setup`.

## Scope and reason

The legacy requirements file attempted to compile `blis==0.7.11` and failed in its isolated NumPy/Cython build environment on Python 3.14. The web app does not import blis. A separate app requirements file installs the packages actually used by the UI, TF-IDF pipeline, voice features, and multilingual module. Research requirements and application code are unchanged.

## Environment and evidence

Validation used Windows x64, Python 3.14.0, and a newly created virtual environment at `%LOCALAPPDATA%\Temp\wil-app-setup-20260926`. The existing project `.venv` was preserved.

- Clean installation of the nine direct app dependencies using binary distributions: PASS.
- Direct versions match `requirements-app.txt`; pip dry-run against that file required no changes: PASS.
- `python -m pip check`: PASS, no broken requirements.
- Imports of Streamlit, pandas, scikit-learn, Ollama, edge-tts, torch, SentencePiece, WhisperModel, and the three Transformers Auto classes used by the app: PASS.
- Existing automated test suite: **14 passed, 1 failed**. Test 05 expects `TRP002` for the Incoming Passenger Card question but current retrieval returns `TRP003` first. The failure is recorded, not hidden by changing the test expectation.
- The same test failure was reproduced in the original `.venv`, confirming it is not specific to the fresh installation.
- Cache inspection found neither multilingual model configuration locally; full startup would require the first-time model downloads.

## Limits and remaining manual validation

Package installation and imports are verified. Full app execution with downloaded models, generated answers, browser microphone recording, and audible speech playback have not been verified in this clean environment. Do not treat the import check as proof that those features work. Follow the README manual checks before the final demonstration.

The multilingual module loads BGE-M3 and NLLB during import. Their initial downloads require several GB and an internet connection. Voice input also downloads Whisper `base` on first use. Ollama must be running with both `llama3.2` and `qwen2.5:3b-instruct` installed. Edge speech playback requires internet access.

The direct dependencies are pinned, but their transitive dependencies are not fully locked. Other operating systems and Python versions have not been validated. The legacy research/evaluation environment is outside this installation check.

## Reproduction

Use the README commands to create `.venv-app`, install `requirements-app.txt`, run `pip check`, and run the existing tests. A failed test must be investigated even if installation succeeded. Keep application and research environments separate.
