from pathlib import Path
import pandas as pd
import shutil


# ============================================================
# FILE PATHS
# ============================================================

# data.py is located inside G14_WIL/data/
# Therefore all of these files are in the same folder.

DATA_FOLDER = Path(__file__).parent

TOPICS_FILE = DATA_FOLDER / "topics.csv"
COLLECTION_FILE = DATA_FOLDER / "collection.csv"
GROUNDTRUTH_FILE = DATA_FOLDER / "groundtruth.csv"
GOLDEN_FILE = DATA_FOLDER / "golden_summaries.csv"
QRELS_FILE = DATA_FOLDER / "qrels.txt"


# ============================================================
# TRAVEL / BIOSECURITY TEST DATA
# ============================================================

travel_data = [

    {
        "topic_id": "TR01",
        "topic": "Goods declaration requirements",
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
        "topic": "Food from aircraft or ships",
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
        "topic": "Arrival process",
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
            "their baggage, and then go to biosecurity inspection with their "
            "declaration and declared goods."
    },

    {
        "topic_id": "TR04",
        "topic": "Baggage inspection",
        "question_id": "TR04Q01",
        "question":
            "Can travellers' bags be checked even if they do not declare any goods?",
        "passage_id": "TRP004",
        "passage":
            "Your bags may be checked by a biosecurity officer, a detector dog "
            "or X-ray, even if you don't declare any goods.",
        "summary":
            "Yes. Bags may be checked by a biosecurity officer, detector dog "
            "or X-ray even when no goods have been declared."
    },

    {
        "topic_id": "TR05",
        "topic": "Failure to declare risk goods",
        "question_id": "TR05Q01",
        "question":
            "What can happen if a traveller fails to declare biosecurity risk goods?",
        "passage_id": "TRP005",
        "passage":
            "If you provide false or misleading information to a biosecurity "
            "officer or on your declaration, or if you fail to answer questions "
            "about the goods or comply with directions given by a biosecurity "
            "officer, you may be given an infringement notice, subject to civil "
            "penalty proceedings, and/or prosecuted for a criminal offence. "
            "Your visa may also be cancelled.",
        "summary":
            "Failure to declare risk goods may result in an infringement notice, "
            "civil penalties or criminal prosecution. A traveller's visa may "
            "also be cancelled."
    },

    {
        "topic_id": "TR06",
        "topic": "Declaring prohibited goods",
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
        "topic": "Declared goods inspection",
        "question_id": "TR07Q01",
        "question":
            "What happens to goods that a traveller declares when entering Australia?",
        "passage_id": "TRP007",
        "passage":
            "A biosecurity officer will inspect your presented goods and may "
            "ask for more information or documentation. If the goods are permitted "
            "and pass inspection they will be returned to you. If the goods do "
            "not pass inspection, you may have to pay to have the goods treated, "
            "exported from Australia or destroyed.",
        "summary":
            "Declared goods are inspected by a biosecurity officer. Goods that "
            "pass inspection are returned, while other goods may need treatment, "
            "export or destruction."
    },

    {
        "topic_id": "TR08",
        "topic": "Outdoor equipment biosecurity",
        "question_id": "TR08Q01",
        "question":
            "Do travellers need to be concerned about contaminated hiking boots "
            "or outdoor equipment?",
        "passage_id": "TRP008",
        "passage":
            "Outdoor, camping and sports equipment and footwear includes hiking "
            "boots, fishing equipment and anything that could be contaminated "
            "with soil, seeds, animal or faecal matter, or freshwater.",
        "summary":
            "Yes. Hiking boots and outdoor equipment contaminated with soil, "
            "seeds, animal matter or freshwater may present a biosecurity risk."
    },

    {
        "topic_id": "TR09",
        "topic": "Biosecurity risks found after arrival",
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
        "topic": "Electronic equipment",
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
        "topic": "Dairy and egg products",
        "question_id": "TR11Q01",
        "question":
            "Do travellers need to declare dairy and egg products when entering Australia?",
        "passage_id": "TRP011",
        "passage":
            "Dairy and egg products include infant formula, cheese, milk and "
            "yoghurt, whole, dry and powdered eggs, mayonnaise, noodles and pasta.",
        "summary":
            "Certain dairy and egg products must be declared, including cheese, "
            "milk, yoghurt and egg products."
    },

    {
        "topic_id": "TR12",
        "topic": "Plant material",
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
        "topic": "Herbs spices and teas",
        "question_id": "TR13Q01",
        "question":
            "Do travellers need to declare herbs, spices or herbal teas when "
            "entering Australia?",
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
        "topic": "Animal products",
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
        "topic": "Checking import conditions",
        "question_id": "TR15Q01",
        "question":
            "How can travellers check whether goods are allowed into Australia "
            "before travelling?",
        "passage_id": "TRP015",
        "passage":
            "Visit agriculture.gov.au/bringing-goods. For specific import "
            "conditions or documentation requirements, visit the Biosecurity "
            "Import Conditions system (BICON). If you need an import permit, "
            "you must apply and receive it before you bring the goods to Australia.",
        "summary":
            "Travellers can check Australian Government bringing-goods guidance "
            "and BICON before travelling. Any required import permit must be "
            "obtained before the goods are brought to Australia."
    }
]


# ============================================================
# CHECK FILES EXIST
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
            f"Could not find: {file_path}"
        )


# ============================================================
# LOAD EXISTING GROUP DATA
# ============================================================

print()
print("Loading existing group data...")

topics_df = pd.read_csv(TOPICS_FILE)
collection_df = pd.read_csv(COLLECTION_FILE)
groundtruth_df = pd.read_csv(GROUNDTRUTH_FILE)
golden_df = pd.read_csv(GOLDEN_FILE)

print(f"Existing topics: {len(topics_df)}")
print(f"Existing passages: {len(collection_df)}")
print(f"Existing ground-truth rows: {len(groundtruth_df)}")
print(f"Existing golden summaries: {len(golden_df)}")


# ============================================================
# VERIFY COLUMN STRUCTURE
# ============================================================

expected_topics = [
    "topic_id",
    "Topic",
    "question_id",
    "question"
]

expected_collection = [
    "passage_id",
    "passage"
]

expected_groundtruth = [
    "topic_id",
    "topic",
    "passage_id",
    "passage",
    "relevance_judgment"
]

expected_golden = [
    "question_id",
    "summary_id",
    "summary",
    "passage_id"
]


if list(topics_df.columns) != expected_topics:
    raise ValueError(
        f"Unexpected topics.csv columns: "
        f"{list(topics_df.columns)}"
    )

if list(collection_df.columns) != expected_collection:
    raise ValueError(
        f"Unexpected collection.csv columns: "
        f"{list(collection_df.columns)}"
    )

if list(groundtruth_df.columns) != expected_groundtruth:
    raise ValueError(
        f"Unexpected groundtruth.csv columns: "
        f"{list(groundtruth_df.columns)}"
    )

if list(golden_df.columns) != expected_golden:
    raise ValueError(
        f"Unexpected golden_summaries.csv columns: "
        f"{list(golden_df.columns)}"
    )

print("CSV structures verified.")


# ============================================================
# DETERMINE WHAT DATA HAS ALREADY BEEN ADDED
# ============================================================

existing_questions = set(
    topics_df["question_id"].astype(str)
)

existing_passages = set(
    collection_df["passage_id"].astype(str)
)

existing_groundtruth = set(
    groundtruth_df["passage_id"].astype(str)
)

existing_golden_questions = set(
    golden_df["question_id"].astype(str)
)


# ============================================================
# GET EXISTING RELEVANCE VALUE
# ============================================================

relevance_values = (
    groundtruth_df["relevance_judgment"]
    .dropna()
)

if len(relevance_values) > 0:
    relevance_value = relevance_values.iloc[0]
else:
    relevance_value = 2

print(
    f"Using relevance judgment: {relevance_value}"
)


# ============================================================
# BUILD NEW ROWS
# ============================================================

new_topics = []
new_collection = []
new_groundtruth = []
new_golden = []


for item in travel_data:

    # ---------------- TOPICS ----------------

    if item["question_id"] not in existing_questions:

        new_topics.append(
            {
                "topic_id": item["topic_id"],
                "Topic": item["topic"],
                "question_id": item["question_id"],
                "question": item["question"]
            }
        )


    # ---------------- COLLECTION ----------------

    if item["passage_id"] not in existing_passages:

        new_collection.append(
            {
                "passage_id": item["passage_id"],
                "passage": item["passage"]
            }
        )


    # ---------------- GROUNDTRUTH ----------------

    if item["passage_id"] not in existing_groundtruth:

        new_groundtruth.append(
            {
                "topic_id": item["topic_id"],
                "topic": item["topic"],
                "passage_id": item["passage_id"],
                "passage": item["passage"],
                "relevance_judgment": relevance_value
            }
        )


    # ---------------- GOLDEN SUMMARIES ----------------

    if item["question_id"] not in existing_golden_questions:

        new_golden.append(
            {
                "question_id": item["question_id"],
                "summary_id": item["passage_id"],
                "summary": item["summary"],
                "passage_id": item["passage_id"]
            }
        )


# ============================================================
# CREATE DATAFRAMES
# ============================================================

new_topics_df = pd.DataFrame(
    new_topics,
    columns=expected_topics
)

new_collection_df = pd.DataFrame(
    new_collection,
    columns=expected_collection
)

new_groundtruth_df = pd.DataFrame(
    new_groundtruth,
    columns=expected_groundtruth
)

new_golden_df = pd.DataFrame(
    new_golden,
    columns=expected_golden
)


# ============================================================
# CREATE BACKUPS
# ============================================================

def backup_file(file_path):

    backup_path = file_path.with_name(
        file_path.stem + "_backup" + file_path.suffix
    )

    if not backup_path.exists():

        shutil.copy(
            file_path,
            backup_path
        )

        print(
            f"Backup created: {backup_path.name}"
        )


print()
print("Creating backups...")

backup_file(TOPICS_FILE)
backup_file(COLLECTION_FILE)
backup_file(GROUNDTRUTH_FILE)
backup_file(GOLDEN_FILE)
backup_file(QRELS_FILE)


# ============================================================
# MERGE CSV DATA
# ============================================================

updated_topics = pd.concat(
    [topics_df, new_topics_df],
    ignore_index=True
)

updated_collection = pd.concat(
    [collection_df, new_collection_df],
    ignore_index=True
)

updated_groundtruth = pd.concat(
    [groundtruth_df, new_groundtruth_df],
    ignore_index=True
)

updated_golden = pd.concat(
    [golden_df, new_golden_df],
    ignore_index=True
)


# ============================================================
# SAVE CSV FILES
# ============================================================

updated_topics.to_csv(
    TOPICS_FILE,
    index=False
)

updated_collection.to_csv(
    COLLECTION_FILE,
    index=False
)

updated_groundtruth.to_csv(
    GROUNDTRUTH_FILE,
    index=False
)

updated_golden.to_csv(
    GOLDEN_FILE,
    index=False
)


# ============================================================
# UPDATE QRELS.TXT
# ============================================================

print()
print("Updating qrels.txt...")


# Read current qrels
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


existing_qrels_set = set(existing_qrels)

new_qrels = []


for item in travel_data:

    qrels_line = (
        f"{item['question_id']} "
        f"0 "
        f"{item['passage_id']} "
        f"2"
    )

    if qrels_line not in existing_qrels_set:
        new_qrels.append(qrels_line)


# Append only new qrels
with open(
    QRELS_FILE,
    "a",
    encoding="utf-8"
) as file:

    for row in new_qrels:
        file.write(row + "\n")


# ============================================================
# FINAL VALIDATION
# ============================================================

final_topics = pd.read_csv(TOPICS_FILE)
final_collection = pd.read_csv(COLLECTION_FILE)
final_groundtruth = pd.read_csv(GROUNDTRUTH_FILE)
final_golden = pd.read_csv(GOLDEN_FILE)


missing_questions = []

for item in travel_data:

    if item["question_id"] not in set(
        final_topics["question_id"].astype(str)
    ):
        missing_questions.append(
            item["question_id"]
        )


if missing_questions:

    raise ValueError(
        f"Missing travel questions after merge: "
        f"{missing_questions}"
    )


# ============================================================
# FINISHED
# ============================================================

print()
print("=" * 60)
print("TRAVEL RAG DATA MERGE COMPLETE")
print("=" * 60)

print()

print(
    f"New topics added: "
    f"{len(new_topics_df)}"
)

print(
    f"New passages added: "
    f"{len(new_collection_df)}"
)

print(
    f"New ground-truth rows added: "
    f"{len(new_groundtruth_df)}"
)

print(
    f"New golden summaries added: "
    f"{len(new_golden_df)}"
)

print(
    f"New qrels added: "
    f"{len(new_qrels)}"
)

print()

print("Current totals:")

print(
    f"topics.csv: "
    f"{len(final_topics)}"
)

print(
    f"collection.csv: "
    f"{len(final_collection)}"
)

print(
    f"groundtruth.csv: "
    f"{len(final_groundtruth)}"
)

print(
    f"golden_summaries.csv: "
    f"{len(final_golden)}"
)

print(
    f"qrels.txt: "
    f"{len(existing_qrels) + len(new_qrels)}"
)

print()
print(
    "All 15 Australian travel questions are present."
)

print("Done.")