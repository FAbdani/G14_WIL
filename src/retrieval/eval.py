from ranx import Qrels, Run, evaluate
import pandas as pd
import numpy as np

pd.set_option('future.infer_string', False)

# Adapted from the Walert retrieval evaluation for our project dataset.
# Walert splits topics into known/inferred sets and compares multiple runs,
# while our current milestone evaluates one TF-IDF baseline across all questions.

# Evaluate all of our project questions using the generated TF-IDF run

QRELS_PATH = "../../data/qrels.txt"
RUN_PATH = "../../target/runs/rag-tfidf.txt"


qrels_df = pd.read_csv(
    QRELS_PATH,
    sep=r"\s+",
    names=["q_id", "zero", "doc_id", "score"]
)
qrels_df["q_id"] = qrels_df["q_id"].to_numpy(dtype=object)
qrels_df["doc_id"] = qrels_df["doc_id"].to_numpy(dtype=object)

qrels = Qrels.from_df(
    qrels_df,
    q_id_col="q_id",
    doc_id_col="doc_id",
    score_col="score"
)

run = Run.from_file(RUN_PATH, kind="trec")

# TF-IDF baseline evaluation using the same nDCG cutoffs as Walert

results = evaluate(
    qrels,
    run,
    metrics=["ndcg@1", "ndcg@3", "ndcg@5"]
)

print("TF-IDF Evaluation Results")
print(results)