from pyserini.search.lucene import LuceneSearcher
import pandas as pd
import ollama


COLLECTION = "../../data/collection.csv"
TOPICS = "../../data/topics.csv"

INDEX = "../../target/indexes/bm25"

searcher = LuceneSearcher(INDEX)

collection_df = pd.read_csv(COLLECTION)

def get_context_passages(question, top_k = 3):
    """Retrieve the top_k most relevant passages for a question using BM25"""
    num_hits = 10
    hits = searcher.search(question, num_hits)
    
    context_passages = []
    for hit in hits[:top_k]:
        matches = collection_df[collection_df['passage_id'] == hit.docid]['passage']
        if not matches.empty:
            context_passages.append(matches.values[0])
            
    return context_passages
    
def generate_answer(question, context):
    """Generate an answer from Ollama grounded in retrieved passaged"""
    static_prompt = (
        "Generate an answer to the following question based on the retrieved documents below."
        "If the retrieved documents are not related to the question, then say: "
        "\"I do not have enough information to answer this question.\""
    )
    
    doc_lines = "\n".join(f"Document {i + 1}: {passage}" for i, passage in enumerate(context))
    
    prompt = f"{static_prompt}\nQuestion: {question}\n{doc_lines}\nAnswer:"
    
    response = ollama.chat(model = 'llama3.2', messages = [
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
    test_question = "What goods must travellers declare before arriving to Australia?"
    result = answer_question(test_question)
    print("Question:", test_question)
    print("Answer:", result)