# counts the number of questions index holds and compares it to the amount collection holds

from pyserini.search.lucene import LuceneSearcher
import pandas as pd

INDEX_PATH = "../../target/indexes/bm25"
COLLECTION_PATH = "../../data/collection.csv"

searcher = LuceneSearcher(INDEX_PATH)
df = pd.read_csv(COLLECTION_PATH)

print("Documents in index:", searcher.num_docs, "| rows in collection.csv:", len(df))

# compares the stored text of one passage with the collection
doc = searcher.doc("TRP004")
print("TRP004 in index:", doc is not None)
if doc is not None:
    print("Index text:", doc.raw()[:300])
print("CSV text:  ", df[df.passage_id == "TRP004"].passage.values[0][:300])

for q in ["SmartGate", "SmartGate ePassport", "arrival airports"]:
    hits = searcher.search(q, 10)
    print(q, "->", [h.docid for h in hits])