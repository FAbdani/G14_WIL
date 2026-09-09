# loading libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import ollama


# file paths
COLLECTION = "../../data/collection.csv"
TOPICS = "../../data/topics.csv"

OUTPUT = "../../target/runs/generated_answers.csv"
MODEL = "llama3.2"

# This is the threshold so below this is it no relevant passages found
MIN_SIMILARITY = 0.05 

# loading the data
collection_df = pd.read_csv(COLLECTION)
topics_df = pd.read_csv(TOPICS)

# building the tfidf search index
vectorizer = TfidfVectorizer(stop_words = 'english')
passage_vectors = vectorizer.fit_transform(collection_df['passage'])

def get_context_passages(question, top_k = 3):
    """Retrieve the top_k most relevant passages for a question using BM25"""
    
    # converting the question into a vector
    question_vector = vectorizer.transform([question])
    # measuring how similar each questio is to a passage
    similarities = cosine_similarity(question_vector, passage_vectors).flatten()

    # gets the indices of the top_k highest-scoring passages
    top_indices = similarities.argsort()[::-1][:top_k]
    
    # only keeps the passages that are above the minimum similarity threshold
    context_passages = []
    for idx in top_indices:
        if similarities[idx] >= MIN_SIMILARITY:
            context_passages.append(collection_df.iloc[idx]['passage'])

    return context_passages
    
def generate_answer(question, context):
    """Generate an answer from Ollama grounded in retrieved passages"""
    static_prompt = (
        "Generate an answer to the following question based on the retrieved documents below."
        "Check each document and use only the relevant document(s) to answer"
        "If the retrieved documents are not related to the question, then say: "
        "\"I do not have enough information to answer this question.\""
    )

    doc_lines = "\n".join(f"Document {i + 1}: {passage}" for i, passage in enumerate(context))
    prompt = f"{static_prompt}\nQuestion: {question}\n{doc_lines}\nAnswer:"

    response = ollama.chat(model=MODEL, messages=[
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
            'question_id' : question_id,
            'question' : question,
            'generated_answer' : answer
        })
        
    results_df = pd.DataFrame(results)
    results_df.to_csv(OUTPUT, index = False)
    print(f"\n {len(results)} answers saved to {OUTPUT}")