# RAG Pipeline Automated Test Results

## Purpose

This document records the automated test evidence for the 15 runnable question-and-answer tests with documented results. The tests cover retrieval accuracy, citation metadata, safe refusal behaviour, answer parsing, pipeline integration, and compatibility with the existing batch interface.

## Testing approach

The retrieval tests use the real `data/collection.csv` knowledge base and the real TF-IDF implementation. This ensures that changes to the collection, ranking, similarity threshold, or citation structure can cause a meaningful test failure.

Ollama is mocked in the automated generation test. A language model can produce different wording for the same prompt and may take a long time to load, so requiring a live model for every test would make the suite slow and unreliable. The mocked test still verifies the important integration contract: retrieved passage text is supplied to generation, the generated response is cleaned, and the answer is returned together with its citation metadata. Five separate live Ollama integration checks are already recorded in `docs/streamlit_pipeline_integration.md`.

## How to run the tests

From the repository root, activate the virtual environment and use Python's built-in `unittest` runner:

```powershell
.\.venv\Scripts\Activate.ps1
python -m unittest discover -s tests -p "test_*.py" -v
```

No additional testing package or Ollama session is required for this automated suite.

## Test cases and results

| # | Test coverage | Expected result | Result |
|---|---|---|---|
| 1 | Electronic Travel Authority question | `VP001` is the primary source | Pass |
| 2 | Frequent Traveller conditions question | `VP002` is the primary source | Pass |
| 3 | Total visitor visas question | `VP003` is selected instead of a stream subtotal | Pass |
| 4 | Passenger travel-document question | `TRP001` is the primary source | Pass |
| 5 | Incoming Passenger Card question | `TRP002` is the primary source | Pass |
| 6 | `top_k=1` retrieval limit | No more than one source is returned | Pass |
| 7 | Citation metadata structure | ID, passage text, and numeric similarity are returned | Pass |
| 8 | Citation relevance ordering | Sources are ordered from highest to lowest score | Pass |
| 9 | Unrelated vocabulary | No unsupported citation is returned | Pass |
| 10 | Existing context wrapper | Passage text matches the richer source results | Pass |
| 11 | Leading `Answer:` label | Label is removed from displayed answer | Pass |
| 12 | `Answer:` occurring inside valid text | Earlier response text is preserved | Pass |
| 13 | No relevant sources | Safe refusal is returned and Ollama is not called | Pass |
| 14 | Retrieval/generation/citation integration | Clean answer and source metadata are returned together | Pass |
| 15 | Existing text-only answer wrapper | A plain answer string is still returned | Pass |

## Execution result

- Execution date: 14 September 2026
- Command: `python -m unittest discover -s tests -p "test_*.py" -v`
- Tests run: 15
- Passed: 15
- Failed: 0
- Errors: 0
- Runtime: 0.065 seconds
- Overall result: **PASS**

## Bugs and observations

No new failures were found during this automated run. The following known behaviour remains documented from live integration testing:

1. Ollama's first live response can be slow while the local model loads.
2. Generated wording is non-deterministic, so factual answer completeness still requires occasional live/manual review.
3. One previous Frequent Traveller response selected the correct source but omitted the three-month-per-visit condition.
4. Questions outside the current collection cannot be answered and should return the safe refusal message without a citation.

## Definition of Done

- [x] 15 test cases created
- [x] Tests are runnable
- [x] Test files created
- [x] Tests run successfully
- [x] Results documented
- [x] Bugs and relevant observations documented
