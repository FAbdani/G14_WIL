import re
import pandas as pd

# ============================================================
# Answer Quality Evaluation (Second Metric)
# ============================================================
#
# The first metric (eval.py) checks whether BM25 retrieval finds the
# right passage (ndcg@k against qrels.txt). This metric goes one step
# further: it checks whether the *generated answer text* produced by
# Ollama actually matches the reference answer written in Sprint 2
# (golden_summaries.csv), regardless of whether retrieval succeeded.
#
# Two scores are computed per question:
#
#   1. ROUGE-L F1 - measures general text overlap between the
#      generated answer and the reference answer, using the Longest
#      Common Subsequence (LCS) of words. This is a standard
#      summarisation/QA metric and needs no extra libraries.
#
#   2. Key Fact Match - unique to this dataset. Many of our
#      questions hinge on getting one specific fact exactly right
#      (a visa subclass number, a stay length, an age range, or a
#      statistic like "5,156,543"). A fluent answer can still be
#      completely wrong on this fact and score reasonably on ROUGE-L
#      alone (this is exactly what happened with VS07Q01, which
#      confidently returned the wrong visa statistic). This score
#      extracts numbers and visa subclass codes from the reference
#      answer and checks what fraction of them appear, verbatim, in
#      the generated answer.
#
# Output: target/runs/answer_quality_eval.csv (per-question scores)
#         plus a printed summary of averages.
# ============================================================

GENERATED_PATH = "../../target/runs/generated_answers.csv"
GOLDEN_PATH = "../../data/golden_summaries.csv"
OUTPUT_PATH = "../../target/runs/answer_quality_eval.csv"

MIN_QUESTIONS_REQUIRED = 15  # Sprint 3 acceptance criteria


def tokenize(text):
    """Lowercase, strip punctuation, split into words."""
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9%,.$/\s]", " ", text)
    return text.split()


def lcs_length(a, b):
    """Longest Common Subsequence length between two token lists."""
    n, m = len(a), len(b)
    if n == 0 or m == 0:
        return 0
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][m]


def rouge_l_f1(generated, reference):
    """ROUGE-L F1 score between a generated answer and a reference answer."""
    gen_tokens = tokenize(generated)
    ref_tokens = tokenize(reference)

    if not gen_tokens or not ref_tokens:
        return 0.0

    lcs = lcs_length(gen_tokens, ref_tokens)

    precision = lcs / len(gen_tokens)
    recall = lcs / len(ref_tokens)

    if precision + recall == 0:
        return 0.0

    f1 = (2 * precision * recall) / (precision + recall)
    return round(f1, 4)


# Matches numbers (with optional commas/decimals, e.g. "5,156,543" or "3")
# and visa subclass style codes (e.g. "subclass 601", "601", "417").
NUMBER_PATTERN = re.compile(r"\d[\d,]*(?:\.\d+)?")


def extract_key_facts(text):
    """Pull out the numbers/codes in a piece of text."""
    return set(NUMBER_PATTERN.findall(str(text)))


def key_fact_match_rate(generated, reference, question):
    """Fraction of the reference answer's key numeric facts that also
    appear, verbatim, in the generated answer.

    Numbers that are already given away in the question itself (e.g. a
    year range like "2025-26" repeated in every question about that
    period) are excluded first, since reproducing them proves nothing
    about whether the model actually answered correctly. Only the facts
    that are genuinely part of the *answer* are checked.

    Returns None if there are no such facts to check (e.g. a purely
    descriptive answer with no distinguishing numbers), so it can be
    excluded from the average rather than counted as a failure.
    """
    question_facts = extract_key_facts(question)
    key_facts = extract_key_facts(reference) - question_facts

    if not key_facts:
        return None

    generated_facts = extract_key_facts(generated)
    matched = key_facts & generated_facts

    return round(len(matched) / len(key_facts), 4)


def main():
    generated_df = pd.read_csv(GENERATED_PATH)
    golden_df = pd.read_csv(GOLDEN_PATH)

    merged_df = generated_df.merge(
        golden_df[["question_id", "summary"]],
        on="question_id",
        how="inner",
    )

    if len(merged_df) == 0:
        raise ValueError(
            "No matching question_ids found between generated_answers.csv "
            "and golden_summaries.csv. Have both files been regenerated "
            "from the same version of topics.csv?"
        )

    results = []

    for _, row in merged_df.iterrows():
        generated_answer = row["generated_answer"]
        reference_answer = row["summary"]

        rouge_score = rouge_l_f1(generated_answer, reference_answer)
        fact_score = key_fact_match_rate(generated_answer, reference_answer, row["question"])

        results.append({
            "question_id": row["question_id"],
            "question": row["question"],
            "rouge_l_f1": rouge_score,
            "key_fact_match_rate": fact_score,
        })

    results_df = pd.DataFrame(results)
    results_df.to_csv(OUTPUT_PATH, index=False)

    # ------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------

    n_questions = len(results_df)
    avg_rouge = results_df["rouge_l_f1"].mean()

    fact_scores = results_df["key_fact_match_rate"].dropna()
    avg_fact_match = fact_scores.mean() if len(fact_scores) > 0 else float("nan")

    print("Answer Quality Evaluation Results")
    print(f"Questions evaluated: {n_questions}")

    if n_questions < MIN_QUESTIONS_REQUIRED:
        print(
            f"WARNING: only {n_questions} questions evaluated, "
            f"below the required minimum of {MIN_QUESTIONS_REQUIRED}."
        )

    print(f"Average ROUGE-L F1: {avg_rouge:.4f}")
    print(
        f"Average Key Fact Match Rate: {avg_fact_match:.4f} "
        f"(over {len(fact_scores)} questions with extractable facts)"
    )
    print(f"\nPer-question results saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()