import json
import pandas as pd

# ============================================================
# Convert collection.csv into collection.jsonl for pyserini
# ============================================================
#
# retrieval/index-bm25.sh builds the BM25 Lucene index from
# data/collection/collection.jsonl, but no script in the repo
# previously converted collection.csv into that format - it
# looks like it was done manually and never checked in.
#
# This script regenerates collection.jsonl from the current
# collection.csv, so the index can be rebuilt from scratch
# after any dataset change (like adding the new TR questions).
#
# Run this BEFORE ./retrieval/index-bm25.sh
# ============================================================

COLLECTION_CSV = "collection.csv"
COLLECTION_JSONL = "collection/collection.jsonl"

collection_df = pd.read_csv(COLLECTION_CSV)

with open(COLLECTION_JSONL, "w", encoding="utf-8") as f:
    for _, row in collection_df.iterrows():
        record = {
            "id": row["passage_id"],
            "contents": row["passage"],
        }
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"Converted {len(collection_df)} passages from {COLLECTION_CSV} to {COLLECTION_JSONL}")