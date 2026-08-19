from pathlib import Path
import pandas as pd


# ============================================================
# FILE PATHS
# ============================================================

# data.py is inside G14_WIL/data/
DATA_FOLDER = Path(__file__).parent

TOPICS_FILE = DATA_FOLDER / "topics.csv"
COLLECTION_FILE = DATA_FOLDER / "collection.csv"
GROUNDTRUTH_FILE = DATA_FOLDER / "groundtruth.csv"
GOLDEN_FILE = DATA_FOLDER / "golden_summaries.csv"
QRELS_FILE = DATA_FOLDER / "qrels.txt"


# ============================================================
# RICHY'S AUSTRALIAN TRAVEL / BIOSECURITY DATA
# ============================================================

travel_data = [

    {
        "topic_id": "TR01",
        "Topic": "Goods declaration requirements",
        "question_id": "TR01Q01",
        "question":
            "What goods must travellers declare before arriving in Australia?",
        "passage_id": "TRP001",
        "passage":
            "Complete your declaration. By law, you must declare any risk goods, "
            "including certain food, plant material and animal products. This includes "
            "goods which are commercially prepared and packaged, home-made, fresh, "
            "dried, cooked, uncooked or frozen, or snacks and ingredients for cooking, "
            "even in small amounts.",
        "summary":
            "Travellers must declare risk goods, including certain food, "
            "plant material and animal products."
    },

    {
        "topic_id": "TR02",
        "Topic": "Food from aircraft or ships",
        "question_id": "TR02Q01",
        "question":
            "What should travellers do with food left over from their plane or ship?",
        "passage_id": "TRP002",
        "passage":
            "Don't take food off the plane or ship.",
        "summary":
            "Travellers should not take food off the plane or ship."
    },

    {
        "topic_id": "TR03",
        "Topic": "Arrival process",
        "question_id": "TR03Q01",
        "question":
            "What steps should travellers follow when they arrive in Australia?",
        "passage_id": "TRP003",
        "passage":
            "Proceed through immigration clearance. Collect your baggage. "
            "Proceed to biosecurity inspection and present your declaration "
            "and the goods you are declaring to the biosecurity officer.",
        "summary":
            "Travellers should proceed through immigration clearance, collect "
            "their baggage, then proceed to biosecurity inspection with their "
            "declaration and declared goods."
    },

    {
        "topic_id": "TR04",
        "Topic": "Baggage inspection",
        "question_id": "TR04Q01",
        "question":
            "Can travellers' bags be checked even if they do not declare any goods?",
        "passage_id": "TRP004",
        "passage":
            "Your bags may be checked by a biosecurity officer, a detector dog "
            "or X-ray, even if you don't declare any goods.",
        "summary":
            "Yes. Bags may be checked by a biosecurity officer, detector dog "
            "or X-ray even if no goods are declared."
    },

    {
        "topic_id": "TR05",
        "Topic": "Failure to declare risk goods",
        "question_id": "TR05Q01",
        "question":
            "What can happen if a traveller fails to declare biosecurity risk goods?",
        "passage_id": "TRP005",
        "passage":
            "If you provide false or misleading information to a biosecurity officer "
            "or on your declaration, or if you fail to answer questions about the goods "
            "or comply with directions given by a biosecurity officer, you may be "
            "given an infringement notice, subject to civil penalty proceedings, "
            "and/or prosecuted for a criminal offence. Your visa may also be cancelled.",
        "summary":
            "A traveller may receive an infringement notice, face civil penalty "
            "proceedings or criminal prosecution. Their visa may also be cancelled."
    },

    {
        "topic_id": "TR06",
        "Topic": "Declaring prohibited goods",
        "question_id": "TR06Q01",
        "question":
            "Will travellers be penalised if they declare goods that are not "
            "allowed into Australia?",
        "passage_id": "TRP006",
        "passage":
            "You will not be penalised under the Biosecurity Act 2015 if you "
            "declare and present all goods, even if they are not allowed into Australia.",
        "summary":
            "Travellers will not be penalised under the Biosecurity Act 2015 "
            "if they declare and present all goods."
    },

    {
        "topic_id": "TR07",
        "Topic": "Declared goods inspection",
        "question_id": "TR07Q01",
        "question":
            "What happens to goods that a traveller declares when entering Australia?",
        "passage_id": "TRP007",
        "passage":
            "A biosecurity officer will inspect your presented goods and may ask "
            "for more information or documentation. If the goods are permitted and "
            "pass inspection they will be returned to you. If the goods do not pass "
            "inspection, you may have to pay to have the goods treated, exported "
            "from Australia or destroyed.",
        "summary":
            "Declared goods are inspected. Goods that pass inspection are returned, "
            "while goods that fail may need to be treated, exported or destroyed."
    },

    {
        "topic_id": "TR08",
        "Topic": "Outdoor equipment biosecurity",
        "question_id": "TR08Q01",
        "question":
            "Do travellers need to be concerned about contaminated hiking boots "
            "or outdoor equipment?",
        "passage_id": "TRP008",
        "passage":
            "Outdoor, camping and sports equipment and footwear includes hiking "
            "boots, fishing equipment and anything that could be contaminated with "
            "soil, seeds, animal or faecal matter, or freshwater.",
        "summary":
            "Yes. Hiking boots and outdoor equipment contaminated with soil, seeds, "
            "animal matter or freshwater may present a biosecurity risk."
    },

    {
        "topic_id": "TR09",
        "Topic": "Biosecurity risks found after arrival",
        "question_id": "TR09Q01",
        "question":
            "What should a traveller do if they discover a biosecurity risk "
            "after arriving in Australia?",
        "passage_id": "TRP009",
        "passage":
            "If you find live animals, insects, soil, plant material or other "
            "risk items when unpacking, phone 1800 798 636. You won't be penalised.",
        "summary":
            "Travellers who discover a biosecurity risk after arrival should "
            "phone 1800 798 636."
    },

    {
        "topic_id": "TR10",
        "Topic": "Electronic equipment",
        "question_id": "TR10Q01",
        "question":
            "Are laptops, phones and cameras considered biosecurity risks?",
        "passage_id": "TRP010",
        "passage":
            "The following goods are not a biosecurity risk: electronic equipment "
            "(including laptops, tablets, phones and cameras).",
        "summary":
            "No. Laptops, tablets, phones and cameras are not considered "
            "biosecurity risks."
    },

    {
        "topic_id": "TR11",
        "Topic": "Dairy and egg products",
        "question_id": "TR11Q01",
        "question":
            "Do travellers need to declare dairy and egg products when entering Australia?",
        "passage_id": "TRP011",
        "passage":
            "Dairy and egg products include infant formula, cheese, milk and yoghurt, "
            "whole, dry and powdered eggs, mayonnaise, noodles and pasta.",
        "summary":
            "Certain dairy and egg products must be declared, including cheese, "
            "milk, yoghurt and egg products."
    },

    {
        "topic_id": "TR12",
        "Topic": "Plant material",
        "question_id": "TR12Q01",
        "question":
            "What types of plant material may need to be declared when entering Australia?",
        "passage_id": "TRP012",
        "passage":
            "Plant material includes live plants, seeds, bulbs and cuttings, "
            "fresh and dried flowers, crafts and ornaments, wooden items, "
            "bark, leaves and straw.",
        "summary":
            "Plant materials that may require declaration include live plants, "
            "seeds, bulbs, flowers, wooden items, bark, leaves and straw."
    },

    {
        "topic_id": "TR13",
        "Topic": "Herbs spices and teas",
        "question_id": "TR13Q01",
        "question":
            "Do travellers need to declare herbs, spices or herbal teas "
            "when entering Australia?",
        "passage_id": "TRP013",
        "passage":
            "Food includes raw and cooked food and ingredients, rice, home-cooked "
            "or commercially packaged meals, honey, herbs and spices, including "
            "herbal teas and medicines, snacks, sandwiches, wraps, rolls and burgers.",
        "summary":
            "Yes. Herbs, spices and herbal teas are among the food products "
            "travellers need to declare."
    },

    {
        "topic_id": "TR14",
        "Topic": "Animal products",
        "question_id": "TR14Q01",
        "question":
            "What animal products may need to be declared when travelling to Australia?",
        "passage_id": "TRP014",
        "passage":
            "Live animals and animal products include eggs and nests, feathers, "
            "bones, horns, skins, animal fur and hair, stuffed animals and birds, "
            "shells and coral, beeswax and other bee products.",
        "summary":
            "Animal products that may need declaration include eggs, feathers, "
            "bones, horns, skins, fur, shells, coral and bee products."
    },

    {
        "topic_id": "TR15",
        "Topic": "Checking import conditions",
        "question_id": "TR15Q01",
        "question":
            "How can travellers check whether goods are allowed into Australia "
            "before travelling?",
        "passage_id": "TRP015",
        "passage":
            "Visit agriculture.gov.au/bringing-goods. For specific import conditions "
            "or documentation requirements, visit the Biosecurity Import Conditions "
            "system (BICON). If you need an import permit, you must apply and receive "
            "it before you bring the goods to Australia.",
        "summary":
            "Travellers can check Australian Government bringing-goods guidance "
            "and BICON. Required import permits must be obtained before bringing "
            "the goods to Australia."
    }
]


# ============================================================
# EXPECTED Walert FILE FORMATS
# ============================================================

TOPICS_COLUMNS = [
    "topic_id",
    "Topic",
    "question_id",
    "question"
]

COLLECTION_COLUMNS = [
    "passage_id",
    "passage"
]

GROUNDTRUTH_COLUMNS = [
    "topic_id",
    "topic",
    "passage_id",
    "passage",
    "relevance_judgment"
]

GOLDEN_COLUMNS = [
    "question_id",
    "summary_id",
    "summary",
    "passage_id"
]


# ============================================================
# CHECK REQUIRED FILES
# ============================================================

required_files = [
    TOPICS_FILE,
    COLLECTION_FILE,
    GROUNDTRUTH_FILE,
    GOLDEN_FILE,
    QRELS_FILE
]

for file_path in required_files:

    if not file_path.exists():
        raise FileNotFoundError(
            f"Missing required file: {file_path}"
        )


# ============================================================
# LOAD CURRENT GROUP DATA
# ============================================================

print()
print("Loading current group datasets...")

topics_df = pd.read_csv(TOPICS_FILE)
collection_df = pd.read_csv(COLLECTION_FILE)
groundtruth_df = pd.read_csv(GROUNDTRUTH_FILE)
golden_df = pd.read_csv(GOLDEN_FILE)


# ============================================================
# VERIFY DARSHANA / WALERT FORMAT
# ============================================================

if list(topics_df.columns) != TOPICS_COLUMNS:
    raise ValueError(
        f"topics.csv is not using the expected format.\n"
        f"Expected: {TOPICS_COLUMNS}\n"
        f"Found: {list(topics_df.columns)}"
    )

if list(collection_df.columns) != COLLECTION_COLUMNS:
    raise ValueError(
        f"collection.csv is not using the expected format.\n"
        f"Expected: {COLLECTION_COLUMNS}\n"
        f"Found: {list(collection_df.columns)}"
    )

if list(groundtruth_df.columns) != GROUNDTRUTH_COLUMNS:
    raise ValueError(
        f"groundtruth.csv is not using the expected format.\n"
        f"Expected: {GROUNDTRUTH_COLUMNS}\n"
        f"Found: {list(groundtruth_df.columns)}"
    )

if list(golden_df.columns) != GOLDEN_COLUMNS:
    raise ValueError(
        f"golden_summaries.csv is not using the expected format.\n"
        f"Expected: {GOLDEN_COLUMNS}\n"
        f"Found: {list(golden_df.columns)}"
    )

print("All CSV files use the required format.")


# ============================================================
# REMOVE OLD RICHY TRAVEL RECORDS
# ============================================================

# This keeps Darshana's VS records and removes old TR records
# so our correctly formatted records can be rebuilt.

topics_df = topics_df[
    ~topics_df["topic_id"]
    .astype(str)
    .str.startswith("TR")
].copy()


collection_df = collection_df[
    ~collection_df["passage_id"]
    .astype(str)
    .str.startswith("TRP")
].copy()


groundtruth_df = groundtruth_df[
    ~groundtruth_df["topic_id"]
    .astype(str)
    .str.startswith("TR")
].copy()


golden_df = golden_df[
    ~golden_df["question_id"]
    .astype(str)
    .str.startswith("TR")
].copy()


# ============================================================
# CREATE CORRECTLY FORMATTED TOPICS
# ============================================================

travel_topics = []

for item in travel_data:

    travel_topics.append(
        {
            "topic_id": item["topic_id"],
            "Topic": item["Topic"],
            "question_id": item["question_id"],
            "question": item["question"]
        }
    )


travel_topics_df = pd.DataFrame(
    travel_topics,
    columns=TOPICS_COLUMNS
)


# ============================================================
# CREATE CORRECTLY FORMATTED COLLECTION
# ============================================================

travel_collection = []

for item in travel_data:

    travel_collection.append(
        {
            "passage_id": item["passage_id"],
            "passage": item["passage"]
        }
    )


travel_collection_df = pd.DataFrame(
    travel_collection,
    columns=COLLECTION_COLUMNS
)


# ============================================================
# CREATE CORRECTLY FORMATTED GROUNDTRUTH
# ============================================================

travel_groundtruth = []

for item in travel_data:

    travel_groundtruth.append(
        {
            "topic_id": item["topic_id"],
            "topic": item["Topic"],
            "passage_id": item["passage_id"],
            "passage": item["passage"],
            "relevance_judgment": 2
        }
    )


travel_groundtruth_df = pd.DataFrame(
    travel_groundtruth,
    columns=GROUNDTRUTH_COLUMNS
)


# ============================================================
# CREATE CORRECTLY FORMATTED GOLDEN SUMMARIES
# ============================================================

travel_golden = []

for item in travel_data:

    travel_golden.append(
        {
            "question_id": item["question_id"],
            "summary_id": item["passage_id"],
            "summary": item["summary"],
            "passage_id": item["passage_id"]
        }
    )


travel_golden_df = pd.DataFrame(
    travel_golden,
    columns=GOLDEN_COLUMNS
)


# ============================================================
# MERGE DARSHANA DATA + RICHY DATA
# ============================================================

topics_final = pd.concat(
    [
        topics_df,
        travel_topics_df
    ],
    ignore_index=True
)


collection_final = pd.concat(
    [
        collection_df,
        travel_collection_df
    ],
    ignore_index=True
)


groundtruth_final = pd.concat(
    [
        groundtruth_df,
        travel_groundtruth_df
    ],
    ignore_index=True
)


golden_final = pd.concat(
    [
        golden_df,
        travel_golden_df
    ],
    ignore_index=True
)


# ============================================================
# UPDATE QRELS
# ============================================================

# Keep Darshana's existing qrels.
# Remove any older Richy TR entries first.

with open(
    QRELS_FILE,
    "r",
    encoding="utf-8"
) as file:

    existing_qrels = [
        line.strip()
        for line in file
        if line.strip()
    ]


darshana_qrels = [
    line
    for line in existing_qrels
    if not line.startswith("TR")
]


travel_qrels = []

for item in travel_data:

    travel_qrels.append(
        f"{item['question_id']} 0 {item['passage_id']} 2"
    )


final_qrels = (
    darshana_qrels
    +
    travel_qrels
)


# ============================================================
# SAVE ALL FILES
# ============================================================

topics_final.to_csv(
    TOPICS_FILE,
    index=False
)


collection_final.to_csv(
    COLLECTION_FILE,
    index=False
)


groundtruth_final.to_csv(
    GROUNDTRUTH_FILE,
    index=False
)


golden_final.to_csv(
    GOLDEN_FILE,
    index=False
)


with open(
    QRELS_FILE,
    "w",
    encoding="utf-8"
) as file:

    for line in final_qrels:
        file.write(line + "\n")


# ============================================================
# VALIDATION
# ============================================================

print()
print("Checking final files...")


# Make sure all 15 Richy questions exist
richy_questions = topics_final[
    topics_final["topic_id"]
    .astype(str)
    .str.startswith("TR")
]


if len(richy_questions) != 15:

    raise ValueError(
        f"Expected 15 Richy travel questions, "
        f"but found {len(richy_questions)}."
    )


# Check Richy's question formatting
for _, row in richy_questions.iterrows():

    if not str(row["question_id"]).startswith("TR"):

        raise ValueError(
            f"Incorrect question ID: {row['question_id']}"
        )


# Make sure topic IDs are unique
if topics_final["topic_id"].duplicated().any():

    duplicates = topics_final[
        topics_final["topic_id"].duplicated(
            keep=False
        )
    ]

    print()
    print("WARNING: Duplicate topic IDs found:")
    print(
        duplicates[
            [
                "topic_id",
                "question_id"
            ]
        ]
    )


# Make sure question IDs are unique
if topics_final["question_id"].duplicated().any():

    raise ValueError(
        "Duplicate question IDs were found."
    )


# Make sure passage IDs are unique
if collection_final["passage_id"].duplicated().any():

    raise ValueError(
        "Duplicate passage IDs were found."
    )


# ============================================================
# DISPLAY FINAL SUMMARY
# ============================================================

darshana_count = len(
    topics_final[
        ~topics_final["topic_id"]
        .astype(str)
        .str.startswith("TR")
    ]
)


richy_count = len(
    topics_final[
        topics_final["topic_id"]
        .astype(str)
        .str.startswith("TR")
    ]
)


print()
print("=" * 60)
print("DATASET FORMATTING COMPLETE")
print("=" * 60)

print()
print(
    f"Existing / Darshana questions: "
    f"{darshana_count}"
)

print(
    f"Richy travel questions: "
    f"{richy_count}"
)

print(
    f"Total questions: "
    f"{len(topics_final)}"
)

print()

print(
    f"topics.csv: "
    f"{len(topics_final)} rows"
)

print(
    f"collection.csv: "
    f"{len(collection_final)} rows"
)

print(
    f"groundtruth.csv: "
    f"{len(groundtruth_final)} rows"
)

print(
    f"golden_summaries.csv: "
    f"{len(golden_final)} rows"
)

print(
    f"qrels.txt: "
    f"{len(final_qrels)} rows"
)

print()

print("Richy's questions now follow:")
print(
    "topic_id,Topic,question_id,question"
)

print()
print("Done.")