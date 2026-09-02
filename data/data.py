from pathlib import Path
import pandas as pd


# ============================================================
# FILE PATHS
# ============================================================

DATA_FOLDER = Path(__file__).parent

TOPICS_FILE = DATA_FOLDER / "topics.csv"
COLLECTION_FILE = DATA_FOLDER / "collection.csv"
GROUNDTRUTH_FILE = DATA_FOLDER / "groundtruth.csv"
GOLDEN_FILE = DATA_FOLDER / "golden_summaries.csv"
QRELS_FILE = DATA_FOLDER / "qrels.txt"


# ============================================================
# RICHY'S AUSTRALIAN TRAVEL DATA
# Entry / border requirements + visa requirements
# (Biosecurity dropped entirely per team decision.
#  VS01 - Electronic Travel Authority stay length, and
#  VS02 - Frequent Traveller stream stay conditions, are already
#  covered by Darshana, so they are intentionally not repeated here.)
# ============================================================

travel_data = [

    # --------------------------------------------------------
    # ENTRY / BORDER REQUIREMENTS (TR01-TR25)
    # Source: Australian Border Force - "Arriving and leaving
    # (At the border)" and "Crossing the border: Overview"
    # --------------------------------------------------------

    {
        "topic_id": "TR01", "Topic": "Travel document requirements",
        "question_id": "TR01Q01",
        "question": "What travel document must all arriving and departing passengers have?",
        "passage_id": "TRP001",
        "passage": "All passengers arriving in or departing Australia must carry a valid passport, or another accepted travel document, when crossing the border.",
        "summary": "A valid passport or other accepted travel document.",
    },
    {
        "topic_id": "TR02", "Topic": "Incoming Passenger Card",
        "question_id": "TR02Q01",
        "question": "What must arriving passengers complete when entering Australia?",
        "passage_id": "TRP002",
        "passage": "Passengers arriving in Australia are required to fill out an Incoming Passenger Card as part of the arrival process.",
        "summary": "An Incoming Passenger Card (IPC).",
    },
    {
        "topic_id": "TR03", "Topic": "Visa requirement for non-citizens",
        "question_id": "TR03Q01",
        "question": "What visa requirement applies to non-citizens entering Australia?",
        "passage_id": "TRP003",
        "passage": "Anyone entering Australia who is not an Australian citizen is required to hold a valid visa at the time of entry.",
        "summary": "Non-citizens must hold a valid visa when they enter Australia.",
    },
    {
        "topic_id": "TR04", "Topic": "Arrival SmartGate eligibility",
        "question_id": "TR04Q01",
        "question": "Who is eligible to use SmartGate on arrival at Australian airports?",
        "passage_id": "TRP004",
        "passage": "Travellers may use SmartGate on arrival if they hold an ePassport, are at least 7 years old, and are taller than 1.1 metres.",
        "summary": "Travellers with an ePassport who are aged 7 or over and taller than 1.1m.",
    },
    {
        "topic_id": "TR05", "Topic": "Departure SmartGate conditions",
        "question_id": "TR05Q01",
        "question": "What conditions apply to using departure SmartGates?",
        "passage_id": "TRP005",
        "passage": "Departure SmartGates can be used by any traveller carrying a valid machine-readable passport who is able to operate the gate independently, without an age or height restriction.",
        "summary": "Any traveller with a valid machine-readable passport who can use the gate independently.",
    },
    {
        "topic_id": "TR06", "Topic": "Registering expensive items before departure",
        "question_id": "TR06Q01",
        "question": "What should travellers do with expensive items like cameras or laptops if they intend to bring them back into Australia?",
        "passage_id": "TRP006",
        "passage": "Travellers taking valuable items such as computers, cameras or video cameras out of Australia, who plan to bring them back in, are advised to register the items with Border Force before departure.",
        "summary": "Register the items with Border Force before leaving Australia.",
    },
    {
        "topic_id": "TR07", "Topic": "Form for registering exported goods",
        "question_id": "TR07Q01",
        "question": "What form is used to register expensive items taken out of Australia?",
        "passage_id": "TRP007",
        "passage": "The B263 'Goods exported in passenger baggage' form is used to register high-value items leaving Australia; it cannot be used together with a Tourist Refund Scheme claim, and items must include identifying details such as serial numbers.",
        "summary": "The B263 Goods Exported in Passenger Baggage form.",
    },
    {
        "topic_id": "TR08", "Topic": "Duty-free goods on departure",
        "question_id": "TR08Q01",
        "question": "What must travellers do with duty-free goods when leaving Australia?",
        "passage_id": "TRP008",
        "passage": "Goods bought duty or tax free within Australia must be carried out of the country and shown for inspection at the point of departure, and may also need to be declared when the traveller returns.",
        "summary": "Take the goods with them, present them for inspection at departure, and possibly declare them on return.",
    },
    {
        "topic_id": "TR09", "Topic": "Passport stamping practice",
        "question_id": "TR09Q01",
        "question": "Does Border Force stamp Australian passports as standard practice?",
        "passage_id": "TRP009",
        "passage": "Border Force officers no longer routinely stamp Australian passports, though a traveller can ask an officer to provide a stamp if they need evidence of travel.",
        "summary": "No, not routinely, but a traveller can request one if they need proof of travel.",
    },
    {
        "topic_id": "TR10", "Topic": "Fingerprint checking at the border",
        "question_id": "TR10Q01",
        "question": "Under what circumstance might a traveller need their fingerprints checked?",
        "passage_id": "TRP010",
        "passage": "Non-citizens arriving in or departing Australia may be required to undergo a fingerprint check, used to confirm identity and help resolve any concerns.",
        "summary": "Non-citizens may be fingerprinted on arrival or departure, to verify identity and resolve concerns.",
    },
    {
        "topic_id": "TR11", "Topic": "Fingerprint scan details",
        "question_id": "TR11Q01",
        "question": "How many fingerprints are scanned during a biometric check, and are the scans kept afterwards?",
        "passage_id": "TRP011",
        "passage": "At least four fingerprints are scanned during a border biometric check; the scans are not kept and are deleted once the check is finished.",
        "summary": "At least four fingerprints; the scans are deleted once the check is complete.",
    },
    {
        "topic_id": "TR12", "Topic": "Camera and phone use at the border",
        "question_id": "TR12Q01",
        "question": "When are passengers permitted to use cameras or mobile phones at the border?",
        "passage_id": "TRP012",
        "passage": "Passengers can generally use cameras or mobile phones at the border, except while undergoing a clearance process or when a Border Force officer has directed them not to.",
        "summary": "At any time, except during clearance or if directed otherwise by an officer.",
    },
    {
        "topic_id": "TR13", "Topic": "Legal power to restrict device use",
        "question_id": "TR13Q01",
        "question": "Under what law can officers direct travellers not to use cameras or phones in a customs controlled area?",
        "passage_id": "TRP013",
        "passage": "The Customs Act 1901 gives officers at international airports the power to direct someone in a customs controlled area to stop using cameras, recording equipment or mobile phones, where doing so could interfere with their duties or pose a border risk.",
        "summary": "The Customs Act 1901.",
    },
    {
        "topic_id": "TR14", "Topic": "Baggage examination and questioning powers",
        "question_id": "TR14Q01",
        "question": "What powers do Border Force officers have regarding baggage examination and questioning of travellers?",
        "passage_id": "TRP014",
        "passage": "Border Force officers hold legislative powers to examine travellers' baggage and question them, to detect breaches of customs, quarantine and other Commonwealth laws, including bringing in or taking out prohibited goods.",
        "summary": "They can examine baggage and question travellers to identify breaches of customs, quarantine and other Commonwealth legislation.",
    },
    {
        "topic_id": "TR15", "Topic": "Passenger risk assessment",
        "question_id": "TR15Q01",
        "question": "How does the Department decide which passengers to examine or search?",
        "passage_id": "TRP015",
        "passage": "Passengers are selected for examination using risk-assessment methods; every border crossing is screened through a combination of intelligence, targeting and profiling techniques.",
        "summary": "Through risk-assessment, intelligence, targeting and profiling techniques.",
    },
    {
        "topic_id": "TR16", "Topic": "Advance passenger processing",
        "question_id": "TR16Q01",
        "question": "What is advance passenger processing?",
        "passage_id": "TRP016",
        "passage": "Airlines send the Department passenger details ahead of a flight's arrival, which are analysed to flag possible risk factors, alongside information drawn from airline reservation systems.",
        "summary": "Airlines supply passenger details before arrival, which the Department analyses for risk factors.",
    },
    {
        "topic_id": "TR17", "Topic": "Legal basis for questioning powers",
        "question_id": "TR17Q01",
        "question": "Under what section of the Customs Act do Border Force officers exercise their questioning powers?",
        "passage_id": "TRP017",
        "passage": "Officers question travellers using powers under Section 195 of the Customs Act 1901, covering matters such as dutiable, excisable or prohibited goods, immigration clearance, wildlife specimens, and currency.",
        "summary": "Section 195 of the Customs Act 1901.",
    },
    {
        "topic_id": "TR18", "Topic": "Types of questions asked at the border",
        "question_id": "TR18Q01",
        "question": "What kinds of questions might a Border Force officer ask a traveller about their baggage?",
        "passage_id": "TRP018",
        "passage": "Officers may ask about what is in the bags, whether the traveller knows the contents, who packed them, where the journey started, and the origin, price and source of any goods.",
        "summary": "Questions can cover what's in the bags, who packed them, where the trip started, and the source and price of any goods.",
    },
    {
        "topic_id": "TR19", "Topic": "Refusing to answer officer questions",
        "question_id": "TR19Q01",
        "question": "What can happen if a traveller refuses to answer an officer's questions?",
        "passage_id": "TRP019",
        "passage": "A traveller who refuses to answer an officer's questions may have their goods physically examined as a result, which can delay their clearance through the border.",
        "summary": "Their goods may be physically examined, which can delay their clearance.",
    },
    {
        "topic_id": "TR20", "Topic": "Baggage examination methods",
        "question_id": "TR20Q01",
        "question": "What methods might a Border Force officer use to examine a traveller's baggage?",
        "passage_id": "TRP020",
        "passage": "Under Section 186 of the Customs Act 1901, officers may open packages, use x-ray or ion-scanning devices, test or analyse goods, count or measure them, use a detector dog, or read documents directly or electronically.",
        "summary": "Opening packages, x-ray or ion scanning, testing goods, counting/measuring, using a detector dog, or reading documents.",
    },
    {
        "topic_id": "TR21", "Topic": "Copying travellers' documents",
        "question_id": "TR21Q01",
        "question": "Under what circumstances may Border Force officers copy a traveller's documents?",
        "passage_id": "TRP021",
        "passage": "After examining an item, an officer may copy a document if they believe it could hold information relevant to prohibited goods, an offence under the Customs Act or a prescribed Act, or certain security matters.",
        "summary": "If the officer believes the document may be relevant to prohibited goods, an offence, or a security matter.",
    },
    {
        "topic_id": "TR22", "Topic": "Definition of a document for border powers",
        "question_id": "TR22Q01",
        "question": "Does the definition of 'document' used for border examinations include information stored on phones and laptops?",
        "passage_id": "TRP022",
        "passage": "For the purposes of these powers, a 'document' includes information held on mobile phones, SIM cards, laptops, personal electronic recorders and computers.",
        "summary": "Yes, it includes information stored on mobile phones, SIM cards, laptops and computers.",
    },
    {
        "topic_id": "TR23", "Topic": "Electronic device retention for examination",
        "question_id": "TR23Q01",
        "question": "How long may an electronic device be retained for forensic examination at the border?",
        "passage_id": "TRP023",
        "passage": "A device held for forensic examination under Section 186 of the Customs Act is kept for as long as is reasonably necessary to complete the examination, and longer if it is found to contain prohibited content.",
        "summary": "For as long as reasonably necessary to complete the examination, longer if prohibited content is found.",
    },
    {
        "topic_id": "TR24", "Topic": "Prioritising device examinations",
        "question_id": "TR24Q01",
        "question": "What factors does Border Force consider when prioritising an electronic device examination?",
        "passage_id": "TRP024",
        "passage": "When deciding how quickly to examine a seized device, Border Force takes into account the traveller's confirmed travel plans, the effect on their employment, and their personal circumstances.",
        "summary": "Confirmed travel plans, the impact on employment, and the traveller's personal circumstances.",
    },
    {
        "topic_id": "TR25", "Topic": "Checking what can be brought into Australia",
        "question_id": "TR25Q01",
        "question": "Where should travellers look to find out what items can be brought into or out of Australia?",
        "passage_id": "TRP025",
        "passage": "Details on what can and can't be brought into or out of Australia, and what needs to be declared, are covered in the Border Force 'Can you bring it in?' section of their website.",
        "summary": "The 'Can you bring it in?' section of the Australian Border Force website.",
    },

    # --------------------------------------------------------
    # VISA REQUIREMENTS (TR26-TR38)
    # Source: Department of Home Affairs visa listing pages.
    # ETA (601) stay length and Frequent Traveller stream stay
    # conditions are already covered by Darshana's VS01/VS02,
    # so they are deliberately not repeated here.
    # --------------------------------------------------------

    {
        "topic_id": "TR26", "Topic": "Visitor visa (600) purpose and stay lengths",
        "question_id": "TR26Q01",
        "question": "What is the Visitor visa (subclass 600) generally used for, and how long can it last?",
        "passage_id": "TRP026",
        "passage": "The Visitor visa (subclass 600) is for people coming as tourists or business visitors, or to visit family, and can be granted for 3, 6 or 12 months.",
        "summary": "Tourism, business visits, or visiting family, for a stay of 3, 6 or 12 months.",
    },
    {
        "topic_id": "TR27", "Topic": "Business Visitor stream work restriction",
        "question_id": "TR27Q01",
        "question": "Does the Visitor visa's Business Visitor stream allow the holder to work in Australia?",
        "passage_id": "TRP027",
        "passage": "To qualify for the Business Visitor stream, an applicant must intend to carry out business visitor activities in Australia; business visitor activities specifically do not include work.",
        "summary": "No, business visitor activities are defined as excluding work.",
    },
    {
        "topic_id": "TR28", "Topic": "eVisitor visa conditions",
        "question_id": "TR28Q01",
        "question": "What are the validity period, stay length and cost of an eVisitor visa (subclass 651)?",
        "passage_id": "TRP028",
        "passage": "An eVisitor (subclass 651) visa allows travel to Australia as often as wanted within a 12-month period, with each visit limited to 3 months, and there is no charge to apply.",
        "summary": "Valid for 12 months with unlimited visits, each capped at 3 months, and free to apply for.",
    },
    {
        "topic_id": "TR29", "Topic": "Student visa purpose",
        "question_id": "TR29Q01",
        "question": "What is the Student visa (subclass 500) for?",
        "passage_id": "TRP029",
        "passage": "The Student visa (subclass 500) allows a person to come to Australia to study full-time at a recognised educational institution.",
        "summary": "Studying full-time at a recognised educational institution in Australia.",
    },
    {
        "topic_id": "TR30", "Topic": "Genuine Student requirement criterion",
        "question_id": "TR30Q01",
        "question": "What must Student visa applicants demonstrate under the Genuine Student requirement?",
        "passage_id": "TRP030",
        "passage": "Applicants for a Student visa lodged on or after 23 March 2024 must satisfy the Genuine Student (GS) criterion, or the GS dependent criterion for secondary applicants, in order for the visa to be granted.",
        "summary": "They must satisfy the Genuine Student (GS) criterion, or the GS dependent criterion for accompanying family members.",
    },
    {
        "topic_id": "TR31", "Topic": "Purpose of the Genuine Student requirement",
        "question_id": "TR31Q01",
        "question": "What is the purpose of the Genuine Student requirement?",
        "passage_id": "TRP031",
        "passage": "The Genuine Student requirement is meant to identify students who, after completing their studies in Australia, may develop skills the country needs and could later apply for permanent residence; wanting to stay on afterwards does not count against an applicant.",
        "summary": "To recognise students who may build needed skills while studying, without penalising them for later wanting permanent residence.",
    },
    {
        "topic_id": "TR32", "Topic": "Working Holiday visa purpose",
        "question_id": "TR32Q01",
        "question": "Who is the Working Holiday visa (subclass 417) designed for?",
        "passage_id": "TRP032",
        "passage": "The Working Holiday visa (subclass 417) is intended for young adults who want to take an extended holiday in Australia and work here to help fund it.",
        "summary": "Young adults wanting an extended holiday in Australia who plan to work to help pay for it.",
    },
    {
        "topic_id": "TR33", "Topic": "First Working Holiday visa age range",
        "question_id": "TR33Q01",
        "question": "What is the standard age range for a first Working Holiday visa (subclass 417)?",
        "passage_id": "TRP033",
        "passage": "A first Working Holiday (subclass 417) visa is generally available to people aged 18 to 30 years old who want to have an extended holiday in Australia and work here to fund the trip.",
        "summary": "18 to 30 years old, for most nationalities.",
    },
    {
        "topic_id": "TR34", "Topic": "UK Working Holiday Maker arrangements",
        "question_id": "TR34Q01",
        "question": "What special arrangements apply to UK passport holders applying for a Working Holiday visa (subclass 417)?",
        "passage_id": "TRP034",
        "passage": "Since 1 July 2023, UK passport holders can apply for a Working Holiday (subclass 417) visa between the ages of 18 and 35 inclusive, and since 1 July 2024 can be granted up to three separate Working Holiday visas without needing to meet any specified work requirements.",
        "summary": "They can apply aged 18-35, and can get up to three Working Holiday visas without meeting specified work requirements.",
    },
    {
        "topic_id": "TR35", "Topic": "Work limit with one employer",
        "question_id": "TR35Q01",
        "question": "How long can a Working Holiday (417) or Work and Holiday (462) visa holder work for a single employer?",
        "passage_id": "TRP035",
        "passage": "A mandatory condition on Working Holiday (subclass 417) and Work and Holiday (subclass 462) visas limits the holder to a maximum of six months' work with any one employer, unless an exemption applies or permission is granted to work longer.",
        "summary": "Up to six months with any one employer, unless an exemption applies or extra permission is granted.",
    },
    {
        "topic_id": "TR36", "Topic": "Study or training limit on Working Holiday Maker visas",
        "question_id": "TR36Q01",
        "question": "How much study or training can a Working Holiday Maker visa holder undertake during their stay?",
        "passage_id": "TRP036",
        "passage": "A mandatory condition on Working Holiday Maker visas limits the holder to a maximum of four months of study or training during their stay in Australia, since study is meant to be incidental rather than the main purpose of the visit.",
        "summary": "Up to four months of study or training, since it must remain incidental to the working holiday.",
    },
    {
        "topic_id": "TR37", "Topic": "First Work and Holiday visa purpose",
        "question_id": "TR37Q01",
        "question": "Who is the first Work and Holiday visa (subclass 462) designed for?",
        "passage_id": "TRP037",
        "passage": "A first Work and Holiday (subclass 462) visa is available to people aged 18 to 30 who want an extended holiday in Australia and plan to work here to help fund it.",
        "summary": "People aged 18 to 30 wanting an extended holiday in Australia, funded partly by working here.",
    },
    {
        "topic_id": "TR38", "Topic": "Passport validity recommendation for Visitor visa",
        "question_id": "TR38Q01",
        "question": "How long is it recommended that a traveller's passport remain valid when applying for a Visitor visa?",
        "passage_id": "TRP038",
        "passage": "On the Visitor visa application form, applicants are strongly advised to hold a passport valid for at least 6 months, noting that the stay period actually granted may end up being shorter than what was requested.",
        "summary": "At least 6 months.",
    },
]


# ============================================================
# EXPECTED Walert FILE FORMATS
# ============================================================

TOPICS_COLUMNS = ["topic_id", "Topic", "question_id", "question"]
COLLECTION_COLUMNS = ["passage_id", "passage"]
GROUNDTRUTH_COLUMNS = ["topic_id", "topic", "passage_id", "passage", "relevance_judgment"]
GOLDEN_COLUMNS = ["question_id", "summary_id", "summary", "passage_id"]


# ============================================================
# CHECK REQUIRED FILES
# ============================================================

required_files = [TOPICS_FILE, COLLECTION_FILE, GROUNDTRUTH_FILE, GOLDEN_FILE, QRELS_FILE]

for file_path in required_files:
    if not file_path.exists():
        raise FileNotFoundError(f"Missing required file: {file_path}")


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
# VERIFY WALERT FORMAT
# ============================================================

if list(topics_df.columns) != TOPICS_COLUMNS:
    raise ValueError(
        f"topics.csv is not using the expected format.\n"
        f"Expected: {TOPICS_COLUMNS}\nFound: {list(topics_df.columns)}"
    )

if list(collection_df.columns) != COLLECTION_COLUMNS:
    raise ValueError(
        f"collection.csv is not using the expected format.\n"
        f"Expected: {COLLECTION_COLUMNS}\nFound: {list(collection_df.columns)}"
    )

if list(groundtruth_df.columns) != GROUNDTRUTH_COLUMNS:
    raise ValueError(
        f"groundtruth.csv is not using the expected format.\n"
        f"Expected: {GROUNDTRUTH_COLUMNS}\nFound: {list(groundtruth_df.columns)}"
    )

if list(golden_df.columns) != GOLDEN_COLUMNS:
    raise ValueError(
        f"golden_summaries.csv is not using the expected format.\n"
        f"Expected: {GOLDEN_COLUMNS}\nFound: {list(golden_df.columns)}"
    )

print("All CSV files use the required format.")


# ============================================================
# REMOVE OLD RICHY (TR) BIOSECURITY RECORDS
# ============================================================
# Keeps Darshana's VS records and removes old TR records so the
# new entry-requirements + visa-requirements TR records can be
# rebuilt in their place.

topics_df = topics_df[~topics_df["topic_id"].astype(str).str.startswith("TR")].copy()
collection_df = collection_df[~collection_df["passage_id"].astype(str).str.startswith("TRP")].copy()
groundtruth_df = groundtruth_df[~groundtruth_df["topic_id"].astype(str).str.startswith("TR")].copy()
golden_df = golden_df[~golden_df["question_id"].astype(str).str.startswith("TR")].copy()


# ============================================================
# CREATE CORRECTLY FORMATTED TOPICS / COLLECTION / GROUNDTRUTH / GOLDEN
# ============================================================

travel_topics_df = pd.DataFrame(
    [{"topic_id": i["topic_id"], "Topic": i["Topic"],
      "question_id": i["question_id"], "question": i["question"]} for i in travel_data],
    columns=TOPICS_COLUMNS,
)

travel_collection_df = pd.DataFrame(
    [{"passage_id": i["passage_id"], "passage": i["passage"]} for i in travel_data],
    columns=COLLECTION_COLUMNS,
)

travel_groundtruth_df = pd.DataFrame(
    [{"topic_id": i["topic_id"], "topic": i["Topic"], "passage_id": i["passage_id"],
      "passage": i["passage"], "relevance_judgment": 2} for i in travel_data],
    columns=GROUNDTRUTH_COLUMNS,
)

travel_golden_df = pd.DataFrame(
    [{"question_id": i["question_id"], "summary_id": i["passage_id"],
      "summary": i["summary"], "passage_id": i["passage_id"]} for i in travel_data],
    columns=GOLDEN_COLUMNS,
)


# ============================================================
# MERGE EXISTING DATA + NEW RICHY DATA
# ============================================================

topics_final = pd.concat([topics_df, travel_topics_df], ignore_index=True)
collection_final = pd.concat([collection_df, travel_collection_df], ignore_index=True)
groundtruth_final = pd.concat([groundtruth_df, travel_groundtruth_df], ignore_index=True)
golden_final = pd.concat([golden_df, travel_golden_df], ignore_index=True)


# ============================================================
# UPDATE QRELS
# ============================================================
# Keep existing (Darshana's) qrels. Remove any older Richy TR
# entries first, then add the new TR entries.

with open(QRELS_FILE, "r", encoding="utf-8") as file:
    existing_qrels = [line.strip() for line in file if line.strip()]

kept_qrels = [line for line in existing_qrels if not line.startswith("TR")]

travel_qrels = [f"{i['question_id']} 0 {i['passage_id']} 2" for i in travel_data]

final_qrels = kept_qrels + travel_qrels


# ============================================================
# SAVE ALL FILES
# ============================================================

topics_final.to_csv(TOPICS_FILE, index=False)
collection_final.to_csv(COLLECTION_FILE, index=False)
groundtruth_final.to_csv(GROUNDTRUTH_FILE, index=False)
golden_final.to_csv(GOLDEN_FILE, index=False)

with open(QRELS_FILE, "w", encoding="utf-8") as file:
    for line in final_qrels:
        file.write(line + "\n")


# ============================================================
# VALIDATION
# ============================================================

print()
print("Checking final files...")

richy_questions = topics_final[topics_final["topic_id"].astype(str).str.startswith("TR")]

if len(richy_questions) != 38:
    raise ValueError(f"Expected 38 Richy questions, but found {len(richy_questions)}.")

for _, row in richy_questions.iterrows():
    if not str(row["question_id"]).startswith("TR"):
        raise ValueError(f"Incorrect question ID: {row['question_id']}")

if topics_final["topic_id"].duplicated().any():
    duplicates = topics_final[topics_final["topic_id"].duplicated(keep=False)]
    print()
    print("WARNING: Duplicate topic IDs found:")
    print(duplicates[["topic_id", "question_id"]])

if topics_final["question_id"].duplicated().any():
    raise ValueError("Duplicate question IDs were found.")

if collection_final["passage_id"].duplicated().any():
    raise ValueError("Duplicate passage IDs were found.")

if len(topics_final) != 50:
    raise ValueError(f"Expected 50 questions total, but found {len(topics_final)}.")


# ============================================================
# DISPLAY FINAL SUMMARY
# ============================================================

other_count = len(topics_final[~topics_final["topic_id"].astype(str).str.startswith("TR")])
richy_count = len(richy_questions)

print()
print("=" * 60)
print("DATASET FORMATTING COMPLETE")
print("=" * 60)
print()
print(f"Existing / Darshana questions: {other_count}")
print(f"Richy travel questions: {richy_count}")
print(f"Total questions: {len(topics_final)}")
print()
print(f"topics.csv: {len(topics_final)} rows")
print(f"collection.csv: {len(collection_final)} rows")
print(f"groundtruth.csv: {len(groundtruth_final)} rows")
print(f"golden_summaries.csv: {len(golden_final)} rows")
print(f"qrels.txt: {len(final_qrels)} rows")
print()
print("Richy's questions now follow: topic_id,Topic,question_id,question")
print()
print("Done.")