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
MANDARIN_LANG = "zho_Hans"
HINDI_LANG = "hin_Deva"

# Retrieve top 10 passages
RETRIEVAL_TOP_K = 10


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
# ============================================================

def retrieve_passages(question):
    """
    Retrieve English passages directly from the original
    Korean, Mandarin, Hindi, or English question.

    No translation happens before retrieval.
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
# ============================================================

def select_best_passage(
    question,
    retrieved_passages,
):
    """
    Ask Qwen to select the passage that most directly
    answers the user's question.
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
The user's question may be written in English, Korean,
Mandarin Chinese, or Hindi.

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

    # Fallback to highest-ranked passage
    return retrieved_passages[0]


# ============================================================
# TRANSLATION HELPER
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
                forced_bos_token_id=target_token_id,
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
# STEP 3 - TRANSLATE QUESTION TO ENGLISH
# ============================================================

def translate_question_to_english(
    question,
    source_lang,
):
    """
    Translate the question into English after retrieval.
    """

    return translate_text(
        question,
        source_lang=source_lang,
        target_lang=ENGLISH_LANG,
    )


# ============================================================
# ENGLISH VALIDATION
# ============================================================

def is_english_output(text):
    """
    Check whether generated output appears to be English.
    """

    if not text.strip():
        return False

    # Korean
    if re.search(r"[\uac00-\ud7af]", text):
        return False

    # Mandarin Chinese
    if re.search(r"[\u4e00-\u9fff]", text):
        return False

    # Hindi / Devanagari
    if re.search(r"[\u0900-\u097f]", text):
        return False

    english_letters = re.findall(
        r"[A-Za-z]",
        text
    )

    return len(english_letters) >= 5


# ============================================================
# STEP 4 - GROUNDED ENGLISH ANSWER
# ============================================================

def generate_answer_once(
    english_question,
    selected_passage,
    retry=False,
):
    """
    Generate one grounded English answer.
    """

    if retry:
        extra_instruction = (
            "IMPORTANT: Return English only. "
            "Do not use Korean, Chinese, or Hindi."
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
    Generate a grounded English answer.

    Retry once if non-English output is detected.
    """

    answer = generate_answer_once(
        english_question,
        selected_passage,
        retry=False,
    )

    if is_english_output(answer):
        return answer, False

    print(
        "English validation failed. "
        "Retrying generation once..."
    )

    retry_answer = generate_answer_once(
        english_question,
        selected_passage,
        retry=True,
    )

    return retry_answer, True


# ============================================================
# STEP 5 - TRANSLATE ANSWER BACK TO ORIGINAL LANGUAGE
# ============================================================

def translate_answer_to_target(
    english_answer,
    target_lang,
):
    """
    Translate the grounded English answer into the
    user's original language.
    """

    return translate_text(
        english_answer,
        source_lang=ENGLISH_LANG,
        target_lang=target_lang,
    )


# ============================================================
# LANGUAGE DETECTION
# ============================================================

def detect_language(text):
    """
    Detect one of the supported languages from user input.
    """

    # Korean
    if re.search(r"[\uac00-\ud7af]", text):
        return "Korean", KOREAN_LANG

    # Hindi
    if re.search(r"[\u0900-\u097f]", text):
        return "Hindi", HINDI_LANG

    # Mandarin Chinese
    if re.search(r"[\u4e00-\u9fff]", text):
        return "Mandarin", MANDARIN_LANG

    # Default to English
    return "English", ENGLISH_LANG


# ============================================================
# FULL MULTILINGUAL PIPELINE
# ============================================================

def process_multilingual_question(question):
    """
    Process a user question end-to-end.

    1. Detect the original language.
    2. Retrieve using the original question.
    3. Translate the question to English if needed.
    4. Select the best passage using the English question.
    5. Generate a grounded English answer.
    6. Translate the answer back to the original language.
    """

    language, lang_code = detect_language(
        question
    )

    # Step 1 - Retrieve using original question
    retrieved = retrieve_passages(
        question
    )

    # Step 2 - Translate question to English if needed
    if lang_code == ENGLISH_LANG:
        english_question = question
    else:
        english_question = translate_question_to_english(
            question,
            lang_code,
        )

    # Step 3 - Select best passage using English question
    selected_passage = retrieved[0]

    # Step 4 - Generate grounded English answer
    english_answer, _ = generate_answer(
        english_question,
        selected_passage,
    )

    # Step 5 - Translate back to original language
    if lang_code == ENGLISH_LANG:
        final_answer = english_answer
    else:
        final_answer = translate_answer_to_target(
            english_answer,
            lang_code,
        )

    print("Detected language:", language)
    print("English question:", english_question)
    print("Selected passage:", selected_passage["passage_id"])
    print("English answer:", english_answer)

    return final_answer

