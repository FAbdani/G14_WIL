from pathlib import Path
import csv


# Geting the folde
folder = Path(__file__).parent

# These are the files that the program will use
topics_file = folder / "topics.csv"
groundtruth_file = folder / "groundtruth.csv"
qrels_file = folder / "qrels.txt"


def create_qrels():
    # Stop the program if one of the input files is missing
    if not topics_file.exists():
        raise FileNotFoundError("Could not find topics.csv")

    if not groundtruth_file.exists():
        raise FileNotFoundError("Could not find groundtruth.csv")


    # Read all the questions from topics.csv
    topics = []

    with open(
        topics_file,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            topics.append(row)


    # Read the correct passage matches from groundtruth.csv
    groundtruth = []

    with open(
        groundtruth_file,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            groundtruth.append(row)


    # Match each question to its correct passage
    qrels = []

    for topic in topics:
        topic_id = topic["topic_id"]
        question_id = topic["question_id"]
        match_found = False

        for answer in groundtruth:
            # The topic IDs need to match
            if answer["topic_id"] == topic_id:
                qrels.append([
                    question_id,
                    "0",
                    answer["passage_id"],
                    answer["relevance_judgment"]
                ])

                match_found = True


        # This helps find a mistake in the CSV files
        if not match_found:
            raise ValueError(
                f"No passage was found for {topic_id}"
            )


    # Write the matches into Walert's qrels format
    with open(
        qrels_file,
        "w",
        encoding="utf-8"
    ) as file:
        for qrel in qrels:
            question_id = qrel[0]
            zero = qrel[1]
            passage_id = qrel[2]
            relevance = qrel[3]

            file.write(
                f"{question_id} {zero} "
                f"{passage_id} {relevance}\n"
            )


    # Show a short summary after the program finishes
    print("Questions read:", len(topics))
    print("Ground-truth mappings read:", len(groundtruth))
    print("Qrels mappings created:", len(qrels))
    print("Created:", qrels_file.name)


# Run the function when data.py is opened directly
if __name__ == "__main__":
    create_qrels()
