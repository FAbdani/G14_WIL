# Standard-library path handling keeps data-file locations reliable regardless
# of whether this module is run directly or imported by the Streamlit app.
from pathlib import Path

import ollama
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Resolve every project file from this module's location. The previous paths
# were interpreted from the terminal's working directory, which meant that
# importing this module from root-level app.py looked outside the repository.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
COLLECTION = PROJECT_ROOT / "data" / "collection.csv"
TOPICS = PROJECT_ROOT / "data" / "topics.csv"
OUTPUT = PROJECT_ROOT / "target" / "runs" / "generated_answers.csv"
MODEL = "llama3.2"

# This is the threshold so below this is it no relevant passages found
MIN_SIMILARITY = 0.05 

# Load the small project knowledge base and evaluation topics once. Reusing
# these objects avoids rebuilding the TF-IDF index for every submitted query.
collection_df = pd.read_csv(COLLECTION)
topics_df = pd.read_csv(TOPICS)

# building the tfidf search index
vectorizer = TfidfVectorizer(stop_words = 'english', ngram_range = (1, 2))
passage_vectors = vectorizer.fit_transform(collection_df['passage'])


def retrieve_sources(question, top_k=3):
    """Retrieve the top_k most relevant passages, along with their similarity scores."""
    
    question_vector = vectorizer.transform([question])
    # Measure how similar the question is to every passage.
    similarities = cosine_similarity(question_vector, passage_vectors).flatten()

    # Sort passage positions from highest to lowest similarity.
    top_indices = similarities.argsort()[::-1][:top_k]

    # Keep only passages that satisfy the team's existing relevance threshold.
    sources = []
    for idx in top_indices:
        if similarities[idx] >= MIN_SIMILARITY:
            row = collection_df.iloc[idx]
            sources.append(
                {
                    "passage_id": str(row["passage_id"]),
                    "passage": str(row["passage"]),
                    "similarity": float(similarities[idx]),
                }
            )

    return sources


def get_context_passages(question, top_k=3):
    """Return passage text only for compatibility with existing code."""

    return [
        source["passage"]
        for source in retrieve_sources(question=question, top_k=top_k)
    ]


def generate_answer(question, context):
    """Generate an answer from Ollama grounded in retrieved passages"""
    static_prompt = (
        "Answer the question using only the retrieved documents below. "
        "Treat the documents as the source of truth and check all of them for the requested fact. "
        "Give a concise answer when any document contains the answer, even if its wording differs from the question. "
        "When the question asks about conditions, include every relevant limit stated in the best-matching document "
        "and preserve its numbers exactly. "
        "Do not add an 'Answer:' label or refer to document numbers in the response. "
        "If none of the retrieved documents contains enough information, say exactly: "
        "\"I do not have enough information to answer this question.\""
    )

    doc_lines = "\n".join(f"Document {i + 1}: {passage}" for i, passage in enumerate(context))
    prompt = f"{static_prompt}\nQuestion: {question}\n{doc_lines}\nAnswer:"

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        # Keep the model loaded after an answer so later questions avoid most of
        # the expensive model-loading delay. Ollama may still unload it when the
        # application or local Ollama service is stopped.
        keep_alive="10m",
    )
    return response['message']['content']

def get_answer(text):
    """Remove an optional leading answer label without discarding valid text.

    Ollama occasionally includes the word ``Answer:`` later in an otherwise
    useful response. Searching the entire response and keeping only what came
    after that word caused valid answers to become blank. We therefore remove
    the label only when it is the actual prefix of the response.
    """

    cleaned_text = text.strip()
    answer_prefix = "answer:"
    if cleaned_text.lower().startswith(answer_prefix):
        return cleaned_text[len(answer_prefix):].strip()
    return cleaned_text

def answer_question_with_sources(question):
    """Return a generated answer together with its retrieved source records.

    The Streamlit layer uses this richer result. Retrieval and generation stay
    in this module so the interface does not duplicate pipeline logic.
    """

    sources = retrieve_sources(question)

    # Refuse without calling Ollama when retrieval found no relevant evidence.
    if not sources:
        return {
            "answer": "I do not have enough information to answer this question.",
            "sources": [],
        }

    # Pass only the retrieved text into the existing generation function.
    context_passages = [source["passage"] for source in sources]
    raw_answer = generate_answer(question, context_passages)

    return {
        "answer": get_answer(raw_answer),
        "sources": sources,
    }


def answer_question(question):
    """Return answer text only for the existing batch-evaluation workflow."""

    return answer_question_with_sources(question)["answer"]

if __name__ == "__main__":
    results = []
    
    for question_id, question in topics_df[['question_id', 'question']].values:
        print(f"Processing {question_id}")
        answer = answer_question(question)
        results.append({
            'question_id' : question_id,
            'question' : question,
            'generated_answer' : answer
        })
        
    results_df = pd.DataFrame(results)
    results_df.to_csv(OUTPUT, index = False)
    print(f"\n {len(results)} answers saved to {OUTPUT}")
