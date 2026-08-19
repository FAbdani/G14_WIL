from pyserini.search.lucene import LuceneSearcher
from pyserini.output_writer import OutputFormat, get_output_writer
import pandas as pd

# Use BM25 only for the baseline retrieval
# Dense retrieval is not included at this stage

TOPICS = "../../data/topics.csv"
INDEX = "../../target/indexes/bm25"
OUTPUT_PATH = "../../target/runs/rag-bm25.txt"

topics = pd.read_csv(TOPICS)

searcher = LuceneSearcher(INDEX)

num_hits = 100

# Save retrieval results in TREC format for evaluation

output_writer = get_output_writer(
    OUTPUT_PATH,
    OutputFormat("trec"),
    "w",
    max_hits=num_hits,
    tag="walert_rag_bm25",
    topics=topics
)

with output_writer:
    for question_id, question in topics[["question_id", "question"]].values:
        hits = searcher.search(question, num_hits)
        output_writer.write(question_id, hits)

print("BM25 search complete.")
print(f"Run file saved to: {OUTPUT_PATH}")