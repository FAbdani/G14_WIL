# Streamlit Pipeline Integration and Test Evidence

## Card scope

This work connects the Streamlit interface to the team's working retrieval and answer-generation pipeline. A submitted question is passed to TF-IDF retrieval, the retrieved passages are supplied to the local Ollama `llama3.2` model, and the generated answer is returned with visible source-passage citations.

**Acceptance criterion:** Typing a question returns a generated answer with visible citations to its source passage.

## Confirmed implementation

- **Interface:** Streamlit (`app.py`)
- **Retrieval:** TF-IDF with cosine similarity (`src/retrieval/rag_system.py`)
- **Answer generation:** local Ollama using `llama3.2`
- **Citation data:** passage ID, full source passage, and retrieval relevance score
- **Knowledge base:** `data/collection.csv`

The UI does not invent a second citation system. It displays the passage metadata already returned by the existing retriever. When the model states that there is not enough information, the UI does not show unrelated retrieved passages as supporting citations.

## Changes made

### `src/retrieval/rag_system.py`

- Made project data paths resolve reliably from the module location.
- Added `retrieve_sources()` so retrieval returns passage IDs, passage text, and similarity scores.
- Kept `get_context_passages()` for compatibility with the existing batch workflow.
- Added `answer_question_with_sources()` for the Streamlit integration.
- Kept `answer_question()` returning plain text so existing code is not broken.
- Kept Ollama loaded for ten minutes between requests to reduce repeated model-loading delays.
- Corrected answer parsing so valid text is not accidentally reduced to a blank response.
- Strengthened the grounding prompt to tell the model to use only retrieved evidence.

### `app.py`

- Connected chat submission and suggested-question buttons to the real pipeline.
- Shows the user's question immediately while the slower local model is working.
- Displays each returned passage in an expandable citation section.
- Shows passage ID, relevance score, and full supporting passage.
- Handles pipeline errors without crashing the Streamlit page.
- Prevents a stale pending question from surviving “Clear conversation”.

### `requirements.txt`

- Added the Python `ollama` client dependency.

## Test environment

- Test date: 13 September 2026
- Platform: Windows
- Python: 3.14
- Streamlit: 1.62.0
- scikit-learn: 1.9.1
- Ollama Python client: 0.6.2
- Local model: `llama3.2:latest`

The five checks below called the real `answer_question_with_sources()` integration, including TF-IDF retrieval and the local Ollama model. They were not mocked.

## Five-question integration results

| # | Question | Result | Primary citation | Time | Status |
|---|---|---|---|---:|---|
| 1 | How long can an Electronic Travel Authority holder stay during each visit? | Up to three months on each visit within the stated 12-month validity period. | `VP001` | 35.17 s | Pass |
| 2 | What are the stay conditions for the Frequent Traveller stream? | Returned the 12 months in any 24-month period condition, but omitted the source's three-month maximum per visit. | `VP002` | 14.55 s | Pass for integration; content bug logged |
| 3 | How many visitor visas were granted in total in 2025-26 to 30 June 2026? | 5,156,543. | `VP003` | 6.79 s | Pass |
| 4 | What travel document must all arriving and departing passengers have? | A valid passport or another accepted travel document. | `TRP001` | 4.01 s | Pass |
| 5 | What must arriving passengers complete when entering Australia? | An Incoming Passenger Card. | `TRP002` | 4.05 s | Pass |

Question 2 was rerun after improving the prompt. It again selected the correct `VP002` passage and returned a grounded answer, but still omitted the three-month-per-visit detail. The focused rerun took 21.23 seconds. This confirms that the remaining problem is generated-answer completeness, not retrieval or citation wiring.

## Bugs and limitations logged

1. **Fixed – blank generated answers:** The response parser previously searched for `Answer:` anywhere in a response and could discard useful text. It now removes that label only when it is at the beginning.
2. **Open – answer completeness:** For the Frequent Traveller question, the model cites the correct passage but can omit one of its two stay limits. Future work could use structured extraction, a stricter prompt, or a larger model.
3. **Expected – first response is slow:** The first request may take roughly 20–40 seconds while Ollama loads the model. Later requests were approximately 4–15 seconds in this run. The UI now immediately displays the user's question and a progress spinner, and the model is kept warm for ten minutes.
4. **Expected – limited question coverage:** Answers are limited to facts in `data/collection.csv`. Broad questions such as “What is the main website?” are not answered because the current collection does not contain the required website URL.
5. **Citation format limitation:** The current dataset contains passage IDs and text but not official source URLs. The interface therefore cites the exact stored passage rather than linking to a webpage.

## How to run locally

From the repository root in PowerShell:
activate ollama:

```powershell
.\.venv\Scripts\Activate.ps1
ollama list
ollama run llama3.2
```
Run the app:
``Terminal:
streamlit run app.py
```


## Definition of Done evidence

- [x] Integration working
- [x] Citations displayed
- [x] Tested with five questions
- [x] Bugs logged

The integration card's Definition of Done is satisfied. The separate card requesting 15 runnable test cases and documented results remains separate future work.
