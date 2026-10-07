from pathlib import Path

import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from ranx import Qrels, Run, evaluate

# File locations
PROJECT_ROOT = Path(__file__).resolve().parents[2]
QRELS_PATH = PROJECT_ROOT / "data" / "qrels.txt"
RUNS = {
    "BM25 (baseline)": PROJECT_ROOT / "target" / "runs" / "rag-bm25.txt",
    "TF-IDF (final)": PROJECT_ROOT / "target" / "runs" / "rag-tfidf.txt",
}
OUT_DIR = PROJECT_ROOT / "target" / "results"
METRICS = ["ndcg@1", "ndcg@3", "ndcg@5"]

OUT_DIR.mkdir(parents=True, exist_ok=True)

# Load the answer key once
qrels_df = pd.read_csv(QRELS_PATH, sep=r"\s+", names=["q_id", "zero", "doc_id", "score"])

qrels_df["q_id"] = qrels_df["q_id"].astype(object)
qrels_df["doc_id"] = qrels_df["doc_id"].astype(object)

qrels = Qrels.from_df(qrels_df, q_id_col="q_id", doc_id_col="doc_id", score_col="score")

scores = {}
for name, run_path in RUNS.items():
    run = Run.from_file(str(run_path), kind="trec")
    scores[name] = evaluate(qrels, run, metrics=METRICS, make_comparable=True)

# Building the comparison table
table = pd.DataFrame(scores).loc[METRICS]
table.index = [m.replace("ndcg", "nDCG") for m in table.index]
names = list(RUNS)
table["Change"] = table[names[1]] - table[names[0]]
table = table.round(3)

print(table.to_string())
table.to_csv(OUT_DIR / "bm25_vs_tfidf.csv")

colours = ["#2a78d6", "#eb6834"]
x = np.arange(len(table))
width = 0.34

fig, ax = plt.subplots(figsize=(8, 5), dpi=200)
for i, (name, colour) in enumerate(zip(names, colours)):
    offset = (i - 0.5) * (width + 0.04)
    bars = ax.bar(x + offset, table[name], width, color=colour, label=name, zorder=3)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.015,
                f"{bar.get_height():.2f}", ha="center", va="bottom",
                fontsize=11, fontweight="bold")

ax.set_xticks(x)
ax.set_xticklabels(table.index, fontsize=12)
ax.set_ylim(0, 1.0)
ax.set_ylabel("nDCG score (higher is better)")
ax.set_title("Retrieval quality: BM25 vs TF-IDF",
            loc="left", fontweight="bold")
ax.yaxis.grid(True, color="#e4e3df", zorder=0)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.legend(frameon=False, loc="upper left", ncol=2)

fig.tight_layout()
fig.savefig(OUT_DIR / "bm25_vs_tfidf.png")
print(f"\nSaved table and graph to {OUT_DIR}")