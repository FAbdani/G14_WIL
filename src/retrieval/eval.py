from ranx import Qrels, Run, evaluate
import pandas as pd

# Adapted from the Walert retrieval evaluation for our project dataset.
# Walert splits topics into known/inferred sets and compares multiple runs,
# while our current milestone evaluates one BM25 baseline across all 27 questions.

# Evaluate all of our project questions using the generated BM25 run

QRELS_PATH = "../../data/qrels.txt"
RUN_PATH = "../../target/runs/rag-bm25.txt"


qrels_df = pd.read_csv(
    QRELS_PATH,
    sep=r"\s+",
    names=["q_id", "zero", "doc_id", "score"]
)

qrels = Qrels.from_df(
    qrels_df,
    q_id_col="q_id",
    doc_id_col="doc_id",
    score_col="score"
)

run = Run.from_file(RUN_PATH, kind="trec")

# Initial BM25 baseline evaluation using the same nDCG cutoffs as Walert

results = evaluate(
    qrels,
    run,
    metrics=["ndcg@1", "ndcg@3", "ndcg@5"]
)

print("BM25 Evaluation Results")
print(results)