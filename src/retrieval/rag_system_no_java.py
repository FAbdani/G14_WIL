import pandas as pd
import ollama
from rank_bm25 import BM25Okapi

# ============================================================
# RAG answer generation - Java-free version
# ============================================================
#
# The original rag_system.py used pyserini (a wrapper around the
# Java Lucene search library) for BM25 retrieval, which requires
# installing a JDK and setting JAVA_HOME. This version replaces
# that retrieval step with rank_bm25, a pure-Python BM25
# implementation, so the whole pipeline runs with `pip install`
# only - no Java, no separate indexing step.
#
# It searches directly over collection.csv in memory each time it
# runs. For a dataset this size (50 passages) that's effectively
# instant, so there's no real downside to skipping the prebuilt
# Lucene index.
#
# Generation (calling Ollama) and prompt logic are unchanged from
# the original rag_system.py.
# ============================================================

COLLECTION = "../../data/collection.csv"
TOPICS = "../../data/topics.csv"
OUTPUT = "../../target/runs/generated_answers.csv"

collection_df = pd.read_csv(COLLECTION)
topics_df = pd.read_csv(TOPICS)

# Build the BM25 index once, in memory, from collection.csv.
# Simple whitespace tokenisation - good enough for BM25 over this
# size and style of passage text.
tokenized_passages = [str(p).lower().split() for p in collection_df["passage"]]
bm25 = BM25Okapi(tokenized_passages)


def get_context_passages(question, top_k=3):
    """Retrieve the top_k most relevant passages for a question using BM25."""
    tokenized_query = question.lower().split()
    scores = bm25.get_scores(tokenized_query)

    top_indices = sorted(
        range(len(scores)), key=lambda i: scores[i], reverse=True
    )[:top_k]

    return [collection_df.iloc[i]["passage"] for i in top_indices]


def generate_answer(question, context):
    """Generate an answer from Ollama grounded in retrieved passages."""
    static_prompt = (
        "Generate an answer to the following question based on the retrieved documents below."
        "Check each document and use only the relevant document(s) to answer"
        "If the retrieved documents are not related to the question, then say: "
        "\"I do not have enough information to answer this question.\""
    )

    doc_lines = "\n".join(f"Document {i + 1}: {passage}" for i, passage in enumerate(context))

    prompt = f"{static_prompt}\nQuestion: {question}\n{doc_lines}\nAnswer:"

    response = ollama.chat(model='llama3.2', messages=[
        {'role': 'user', 'content': prompt}
    ])
    return response['message']['content']


def get_answer(text):
    """Extract just the answer portion if the model echoes 'Answer:' back."""
    index = text.find('Answer:')
    if index != -1:
        return text[index + len('Answer:'):].strip()
    return text.strip()


def answer_question(question):
    context_passages = get_context_passages(question)

    if not context_passages:
        return "I apologize, I have no knowledge about that"

    raw_answer = generate_answer(question, context_passages)
    return get_answer(raw_answer)


if __name__ == "__main__":
    results = []

    for question_id, question in topics_df[['question_id', 'question']].values:
        print(f"Processing {question_id}")
        answer = answer_question(question)
        results.append({
            'question_id': question_id,
            'question': question,
            'generated_answer': answer
        })

    results_df = pd.DataFrame(results)
    results_df.to_csv(OUTPUT, index=False)
    print(f"\nDone. {len(results)} answers saved to {OUTPUT}")