from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

COLLECTION = "../../data/collection.csv"
TOPICS = "../../data/topics.csv"
OUTPUT = "../../target/runs/rag-tfidf.txt"

collection_df = pd.read_csv(COLLECTION)
topics_df = pd.read_csv(TOPICS)

vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
passage_vectors = vectorizer.fit_transform(collection_df['passage'])

with open(OUTPUT, "w", encoding="utf-8") as f:
    for question_id, question in topics_df[['question_id', 'question']].values:
        question_vector = vectorizer.transform([question])
        similarities = cosine_similarity(question_vector, passage_vectors).flatten()
        ranked_indices = similarities.argsort()[::-1]
        for rank, idx in enumerate(ranked_indices, start=1):
            passage_id = collection_df.iloc[idx]['passage_id']
            score = similarities[idx]
            f.write(f"{question_id} 0 {passage_id} {rank} {score:.6f} tfidf\n")

print(f"TF-IDF run file written to {OUTPUT}")