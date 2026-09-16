r"""Automated tests for the retrieval and answer-generation integration.

Run from the repository root in PowerShell with:
    .\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v

The suite uses the real project collection for retrieval tests so it detects
accidental changes to passage selection and citation metadata. Ollama is mocked
only where generation is involved. A local language model can vary its wording
and take many seconds to load, so calling it in every automated test would make
the suite slow and non-deterministic.
"""

import unittest
from unittest.mock import patch

from src.retrieval import rag_system


class RetrievalTests(unittest.TestCase):
    """Check that representative questions retrieve the intended evidence."""

    def assert_primary_passage(self, question, expected_passage_id):
        """Assert the highest-ranked citation for a question.

        This helper first checks that evidence exists, producing a useful error
        instead of an unclear list-index failure if retrieval ever breaks.
        """

        sources = rag_system.retrieve_sources(question)
        self.assertGreater(len(sources), 0, "The question returned no sources.")
        self.assertEqual(sources[0]["passage_id"], expected_passage_id)

    def test_01_eta_question_retrieves_eta_passage(self):
        """The ETA stay-length question should cite the ETA passage first."""

        self.assert_primary_passage(
            "How long can an Electronic Travel Authority holder stay during each visit?",
            "VP001",
        )

    def test_02_frequent_traveller_retrieves_conditions(self):
        """The Frequent Traveller question should cite its conditions passage."""

        self.assert_primary_passage(
            "What are the stay conditions for the Frequent Traveller stream?",
            "VP002",
        )

    def test_03_visitor_total_retrieves_total_passage(self):
        """The total visitor-visa question should not select a stream subtotal."""

        self.assert_primary_passage(
            "How many visitor visas were granted in total in 2025-26 to 30 June 2026?",
            "VP003",
        )

    def test_04_travel_document_retrieves_passport_passage(self):
        """The border-document question should retrieve the passport evidence."""

        self.assert_primary_passage(
            "What travel document must all arriving and departing passengers have?",
            "TRP001",
        )

    def test_05_arrival_card_retrieves_passenger_card_passage(self):
        """The arrival-form question should retrieve the Incoming Passenger Card."""

        self.assert_primary_passage(
            "What must arriving passengers complete when entering Australia?",
            "TRP002",
        )

    def test_06_top_k_limits_number_of_sources(self):
        """A caller requesting one source must never receive more than one."""

        sources = rag_system.retrieve_sources(
            "How long can an Electronic Travel Authority holder stay?", top_k=1
        )
        self.assertEqual(len(sources), 1)

    def test_07_source_contains_citation_metadata(self):
        """Every UI citation needs an ID, readable passage, and numeric score."""

        source = rag_system.retrieve_sources(
            "What travel document must passengers have?", top_k=1
        )[0]
        self.assertEqual(set(source), {"passage_id", "passage", "similarity"})
        self.assertIsInstance(source["passage_id"], str)
        self.assertIsInstance(source["passage"], str)
        self.assertIsInstance(source["similarity"], float)

    def test_08_sources_are_sorted_by_relevance(self):
        """Citation scores should be ordered from most to least relevant."""

        sources = rag_system.retrieve_sources(
            "What are the stay conditions for visa travellers?"
        )
        scores = [source["similarity"] for source in sources]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_09_unrelated_vocabulary_returns_no_sources(self):
        """Words absent from the collection should not create false citations."""

        sources = rag_system.retrieve_sources("quasar photosynthesis xylophone")
        self.assertEqual(sources, [])

    def test_10_context_wrapper_returns_only_passage_text(self):
        """The compatibility wrapper must keep returning the original text list."""

        question = "What is an Incoming Passenger Card?"
        sources = rag_system.retrieve_sources(question)
        context = rag_system.get_context_passages(question)
        self.assertEqual(context, [source["passage"] for source in sources])


class AnswerHandlingTests(unittest.TestCase):
    """Check deterministic answer parsing and pipeline coordination."""

    def test_11_leading_answer_label_is_removed(self):
        """A model-added label should not appear in the user-facing response."""

        self.assertEqual(
            rag_system.get_answer("Answer: A valid passport is required."),
            "A valid passport is required.",
        )

    def test_12_internal_answer_word_is_preserved(self):
        """An internal 'Answer:' must not cause earlier valid text to be deleted."""

        response = "The evidence is sufficient. Answer: A passport is required."
        self.assertEqual(rag_system.get_answer(response), response)

    @patch("src.retrieval.rag_system.generate_answer")
    @patch("src.retrieval.rag_system.retrieve_sources", return_value=[])
    def test_13_no_sources_returns_refusal_without_ollama(
        self, mocked_retrieve_sources, mocked_generate_answer
    ):
        """No evidence should produce a safe refusal without calling the model."""

        result = rag_system.answer_question_with_sources("unanswerable question")
        self.assertEqual(
            result["answer"],
            "I do not have enough information to answer this question.",
        )
        self.assertEqual(result["sources"], [])
        mocked_retrieve_sources.assert_called_once_with("unanswerable question")
        mocked_generate_answer.assert_not_called()

    @patch(
        "src.retrieval.rag_system.generate_answer",
        return_value="Answer: Passengers must carry a valid passport.",
    )
    @patch("src.retrieval.rag_system.retrieve_sources")
    def test_14_pipeline_returns_generated_answer_and_citations(
        self, mocked_retrieve_sources, mocked_generate_answer
    ):
        """The integrated result should combine generation with citation data."""

        expected_sources = [
            {
                "passage_id": "TRP001",
                "passage": "Passengers must carry a valid passport.",
                "similarity": 0.75,
            }
        ]
        mocked_retrieve_sources.return_value = expected_sources
        result = rag_system.answer_question_with_sources("What document is needed?")

        self.assertEqual(result["answer"], "Passengers must carry a valid passport.")
        self.assertEqual(result["sources"], expected_sources)
        mocked_generate_answer.assert_called_once_with(
            "What document is needed?", ["Passengers must carry a valid passport."]
        )

    @patch("src.retrieval.rag_system.answer_question_with_sources")
    def test_15_text_only_wrapper_preserves_existing_interface(self, mocked_pipeline):
        """Older batch code should still receive a plain answer string."""

        mocked_pipeline.return_value = {
            "answer": "The required answer.",
            "sources": [{"passage_id": "TEST"}],
        }
        answer = rag_system.answer_question("Example question")
        self.assertEqual(answer, "The required answer.")
        mocked_pipeline.assert_called_once_with("Example question")


if __name__ == "__main__":
    # This entry point supports both direct execution and unittest discovery.
    unittest.main(verbosity=2)
