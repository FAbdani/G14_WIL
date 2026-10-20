# check that for each of the 50 questions, the indexed test correctly matches the passages in the collection
from pyserini.search.lucene import LuceneSearcher
import pandas as pd

searcher = LuceneSearcher("../../target/indexes/bm25")
topics = pd.read_csv("../../data/topics.csv")
coll = pd.read_csv("../../data/collection.csv").set_index("passage_id")["passage"]

# gold passage for each question which is read from qrels
gold = {}
for line in open("../../data/qrels.txt"):
    qid, _, pid, rel = line.split()
    if int(rel) > 0:
        gold[qid] = pid

for qid, q in topics[["question_id", "question"]].values:
    pid = gold[qid]
    doc = searcher.doc(pid)
    same = doc is not None and coll[pid][:60] in doc.raw()
    ids = [h.docid for h in searcher.search(q, 10)]
    rank = ids.index(pid) + 1 if pid in ids else None
    print(f"{qid}  index_matches_csv={same}  gold_rank={rank}")