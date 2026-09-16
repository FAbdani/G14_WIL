from pathlib import Path
import re

import pandas as pd
import torch
import torch.nn.functional as F
import ollama

from transformers import (
    AutoTokenizer,
    AutoModel,
    AutoModelForSeq2SeqLM,
)


# ============================================================
# SETTINGS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
COLLECTION = BASE_DIR.parent.parent / "data" / "collection.csv"

# Multilingual retrieval
RETRIEVER_MODEL_NAME = "BAAI/bge-m3"

# Local LLM
GENERATOR_MODEL_NAME = "qwen2.5:3b-instruct"

# Multilingual translation
TRANSLATOR_MODEL_NAME = "facebook/nllb-200-distilled-600M"

# NLLB language codes
ENGLISH_LANG = "eng_Latn"
KOREAN_LANG = "kor_Hang"

# Small corpus: retrieve broadly for recall
RETRIEVAL_TOP_K = 10


# ============================================================
# TEST CASES
# ============================================================

TEST_CASES = [
    {
        "question_id": "TR01Q01",
        "question": (
            "호주에 도착하기 전에 여행자는 "
            "어떤 물품을 신고해야 하나요?"
        ),
        "expected_passage_id": "TRP001",
    },
    {
        "question_id": "TR13Q01",
        "question": (
            "호주에 입국할 때 허브, 향신료 또는 "
            "허브차를 신고해야 하나요?"
        ),
        "expected_passage_id": "TRP013",
    },
    {
        "question_id": "TR14Q01",
        "question": (
            "호주로 여행할 때 어떤 동물성 제품을 "
            "신고해야 하나요?"
        ),
        "expected_passage_id": "TRP014",
    },
]


# ============================================================
# LOAD COLLECTION
# ============================================================

collection_df = pd.read_csv(COLLECTION)


# ============================================================
# LOAD BGE-M3
# ============================================================

print("Loading BGE-M3 multilingual retriever...")

retriever_tokenizer = AutoTokenizer.from_pretrained(
    RETRIEVER_MODEL_NAME
)

retriever_model = AutoModel.from_pretrained(
    RETRIEVER_MODEL_NAME
)

retriever_model.eval()


# ============================================================
# LOAD NLLB
# ============================================================

print("Loading NLLB translator...")

translator_tokenizer = AutoTokenizer.from_pretrained(
    TRANSLATOR_MODEL_NAME,
    src_lang=ENGLISH_LANG,
)

translator_model = AutoModelForSeq2SeqLM.from_pretrained(
    TRANSLATOR_MODEL_NAME
)

translator_model.eval()

print("NLLB translator loaded.")


# ============================================================
# EMBEDDINGS
# ============================================================

def create_embeddings(texts):
    """
    Create normalized BGE-M3 embeddings.
    """

    encoded = retriever_tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt",
    )

    with torch.no_grad():
        outputs = retriever_model(**encoded)

    embeddings = outputs.last_hidden_state[:, 0]

    return F.normalize(
        embeddings,
        p=2,
        dim=1,
    )


# ============================================================
# CREATE PASSAGE EMBEDDINGS
# ============================================================

print("Creating passage embeddings...")

passage_embeddings = create_embeddings(
    collection_df["passage"]
    .astype(str)
    .tolist()
)

print(
    f"{len(passage_embeddings)} passage embeddings created."
)


# ============================================================
# STEP 1 - MULTILINGUAL RETRIEVAL
#
# Original Korean query -> English knowledge base
# No translation before retrieval.
# ============================================================

def retrieve_passages(question):
    """
    Retrieve English passages directly from the original
    Korean question using BGE-M3.
    """

    query_embedding = create_embeddings(
        [question]
    )

    scores = torch.matmul(
        query_embedding,
        passage_embeddings.T,
    )[0]

    top_results = torch.topk(
        scores,
        k=min(
            RETRIEVAL_TOP_K,
            len(collection_df),
        ),
    )

    results = []

    for score, index in zip(
        top_results.values,
        top_results.indices,
    ):

        row = collection_df.iloc[
            index.item()
        ]

        results.append(
            {
                "passage_id": row["passage_id"],
                "passage": row["passage"],
                "score": float(score),
            }
        )

    return results


# ============================================================
# STEP 2 - QWEN PASSAGE SELECTION
#
# Qwen selects one passage from BGE-M3 top 10.
# ============================================================

def select_best_passage(
    question,
    retrieved_passages,
):
    """
    Ask Qwen to select the single passage that most
    directly answers the Korean question.
    """

    passage_text = "\n\n".join(
        (
            f"[{item['passage_id']}]\n"
            f"{item['passage']}"
        )
        for item in retrieved_passages
    )

    system_prompt = (
        "You are a passage selection system. "
        "Choose the ONE passage that most directly "
        "answers the user's question. "
        "Do not answer the question. "
        "Return only one passage ID."
    )

    user_prompt = f"""
The user's question is written in Korean.
The candidate passages are written in English.

Choose the ONE passage that most directly contains
the information needed to answer the question.

Rules:
1. Do not answer the question.
2. Do not explain your decision.
3. Return ONLY one passage ID.
4. The passage ID must be one of the IDs below.

Question:
{question}

Candidate passages:
{passage_text}

Best passage ID:
"""

    response = ollama.chat(
        model=GENERATOR_MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        options={
            "temperature": 0,
            "num_predict": 20,
        },
    )

    selected_text = (
        response["message"]["content"]
        .strip()
    )

    for item in retrieved_passages:
        if item["passage_id"] in selected_text:
            return item

    # Fallback
    return retrieved_passages[0]


# ============================================================
# NLLB TRANSLATION HELPER
# ============================================================

def translate_text(
    text,
    source_lang,
    target_lang,
):
    """
    Translate text between NLLB-supported languages.
    """

    translator_tokenizer.src_lang = source_lang

    inputs = translator_tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512,
    )

    if hasattr(
        translator_tokenizer,
        "lang_code_to_id",
    ):
        target_token_id = (
            translator_tokenizer
            .lang_code_to_id[target_lang]
        )
    else:
        target_token_id = (
            translator_tokenizer
            .convert_tokens_to_ids(
                target_lang
            )
        )

    with torch.no_grad():
        translated_tokens = (
            translator_model.generate(
                **inputs,
                forced_bos_token_id=(
                    target_token_id
                ),
                num_beams=5,
                max_new_tokens=256,
                early_stopping=True,
            )
        )

    translated_text = (
        translator_tokenizer.decode(
            translated_tokens[0],
            skip_special_tokens=True,
        )
    )

    return translated_text.strip()


# ============================================================
# STEP 3 - TRANSLATE QUESTION
#
# This happens AFTER retrieval and passage selection.
# Korean -> English
# ============================================================

def translate_question_to_english(
    korean_question,
):
    """
    Translate the Korean question into English for
    grounded answer generation.

    This translation does NOT affect first-stage retrieval.
    """

    return translate_text(
        korean_question,
        source_lang=KOREAN_LANG,
        target_lang=ENGLISH_LANG,
    )


# ============================================================
# ENGLISH VALIDATION
# ============================================================

def is_english_output(text):
    """
    Lightweight validation to catch non-English output.
    """

    if not text.strip():
        return False

    # Korean
    if re.search(r"[\uac00-\ud7af]", text):
        return False

    # Japanese Hiragana / Katakana
    if re.search(r"[\u3040-\u30ff]", text):
        return False

    # Chinese / Japanese ideographs
    if re.search(r"[\u4e00-\u9fff]", text):
        return False

    english_letters = re.findall(
        r"[A-Za-z]",
        text
    )

    return len(english_letters) >= 5


# ============================================================
# STEP 4 - GROUNDED ENGLISH ANSWER
#
# Qwen now sees:
# English question + English evidence
# ============================================================

def generate_answer_once(
    english_question,
    selected_passage,
    retry=False,
):
    """
    Generate one grounded English answer attempt.
    """

    if retry:
        extra_instruction = (
            "IMPORTANT: Return English only. "
            "Do not use any non-English language."
        )
    else:
        extra_instruction = (
            "Return the answer in English only."
        )

    system_prompt = (
        "You are a strict evidence-grounded "
        "question-answering assistant. "
        "Use only the supplied evidence. "
        "Never use outside knowledge. "
        "Never invent or reverse facts. "
        "Return only the final answer in English."
    )

    user_prompt = f"""
Answer the English question using ONLY the English evidence below.

{extra_instruction}

Rules:
1. Use only facts explicitly stated in the evidence.
2. Do not add outside information.
3. Do not reverse the meaning of the evidence.
4. Preserve important details and lists accurately.
5. Use simple, clear English.
6. Do not mention the passage ID.
7. Do not explain your reasoning.
8. Return ONLY the final English answer.

English question:
{english_question}

English evidence:
{selected_passage["passage"]}

Final English answer:
"""

    response = ollama.chat(
        model=GENERATOR_MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        options={
            "temperature": 0,
            "num_predict": 160,
        },
    )

    return (
        response["message"]["content"]
        .strip()
    )


def generate_answer(
    english_question,
    selected_passage,
):
    """
    Generate grounded English answer.

    Retry once only if language validation fails.
    """

    answer = generate_answer_once(
        english_question,
        selected_passage,
        retry=False,
    )

    if is_english_output(answer):
        return answer, False

    print(
        "\nEnglish validation failed. "
        "Retrying generation once..."
    )

    retry_answer = generate_answer_once(
        english_question,
        selected_passage,
        retry=True,
    )

    return retry_answer, True


# ============================================================
# STEP 5 - FINAL KOREAN TRANSLATION
#
# English grounded answer -> Korean
# ============================================================

def translate_answer_to_korean(
    english_answer,
):
    """
    Translate grounded English answer into Korean.
    """

    return translate_text(
        english_answer,
        source_lang=ENGLISH_LANG,
        target_lang=KOREAN_LANG,
    )


# ============================================================
# RUN TESTS
# ============================================================

if __name__ == "__main__":

    retrieval_success_count = 0
    selection_success_count = 0
    generation_retry_count = 0

    for test in TEST_CASES:

        question_id = test["question_id"]
        korean_question = test["question"]
        expected = test[
            "expected_passage_id"
        ]

        print("\n")
        print("=" * 70)
        print(question_id)
        print("=" * 70)

        print("\nOriginal Korean question:")
        print(korean_question)


        # ----------------------------------------------------
        # STEP 1 - BGE-M3 RETRIEVAL
        # ----------------------------------------------------

        retrieved = retrieve_passages(
            korean_question
        )

        print("\nRetrieved passages:")

        for i, item in enumerate(
            retrieved,
            start=1,
        ):

            print(
                f"\nRank {i}: "
                f"{item['passage_id']} "
                f"(score={item['score']:.4f})"
            )

            print(
                item["passage"]
            )


        # ----------------------------------------------------
        # RETRIEVAL TEST
        # ----------------------------------------------------

        retrieved_ids = [
            item["passage_id"]
            for item in retrieved
        ]

        if expected in retrieved_ids:

            retrieval_rank = (
                retrieved_ids.index(
                    expected
                )
                + 1
            )

            retrieval_success_count += 1

            print(
                f"\nRetrieval SUCCESS: "
                f"{expected} at rank "
                f"{retrieval_rank}"
            )

        else:

            print(
                f"\nRetrieval FAILED: "
                f"{expected} not found "
                f"in top-{RETRIEVAL_TOP_K}"
            )

            continue


        # ----------------------------------------------------
        # STEP 2 - SELECT BEST PASSAGE
        # ----------------------------------------------------

        selected_passage = (
            select_best_passage(
                korean_question,
                retrieved,
            )
        )

        print("\nSelected passage:")
        print(
            selected_passage[
                "passage_id"
            ]
        )

        print(
            selected_passage[
                "passage"
            ]
        )


        # ----------------------------------------------------
        # SELECTION TEST
        # ----------------------------------------------------

        if (
            selected_passage[
                "passage_id"
            ]
            == expected
        ):

            selection_success_count += 1

            print(
                f"\nSelection SUCCESS: "
                f"{expected}"
            )

        else:

            print(
                f"\nSelection WARNING: "
                f"expected {expected}, "
                f"but selected "
                f"{selected_passage['passage_id']}"
            )


        # ----------------------------------------------------
        # STEP 3 - KOREAN QUESTION -> ENGLISH
        # ----------------------------------------------------

        english_question = (
            translate_question_to_english(
                korean_question
            )
        )

        print(
            "\nTranslated English question:"
        )

        print(
            english_question
        )


        # ----------------------------------------------------
        # STEP 4 - GROUNDED ENGLISH ANSWER
        # ----------------------------------------------------

        english_answer, was_retried = (
            generate_answer(
                english_question,
                selected_passage,
            )
        )

        if was_retried:
            generation_retry_count += 1

        print(
            "\nGrounded English answer:"
        )

        print(
            english_answer
        )


        # ----------------------------------------------------
        # STEP 5 - ENGLISH ANSWER -> KOREAN
        # ----------------------------------------------------

        korean_answer = (
            translate_answer_to_korean(
                english_answer
            )
        )

        print(
            "\nFinal Korean answer:"
        )

        print(
            korean_answer
        )


    # ========================================================
    # SUMMARY
    # ========================================================

    print("\n")
    print("=" * 70)
    print(
        "MULTILINGUAL PIPELINE SUMMARY"
    )
    print("=" * 70)

    print(
        f"\nRelevant passage retrieved: "
        f"{retrieval_success_count}"
        f"/{len(TEST_CASES)}"
    )

    print(
        f"Correct passage selected: "
        f"{selection_success_count}"
        f"/{len(TEST_CASES)}"
    )

    print(
        f"English generation retries: "
        f"{generation_retry_count}"
    )