# G14_WIL

## Team Assignments

| Name   | Student ID        |
|--------|--------------------|
| Fatima Abdani | s4100500 |
| Kashaf Fatima | s4104802  | 
| Darshana Gorantla | s4165839 |
| Jennie Lee | s4077970 |  
| Richy Naveenoa | s4178251  | 

python -m streamlit run app.py

How to run ollama:
1. Go to ollama.com
2. Download it and run the installer
3. Once it is downloade,d run ollama --version in the terminal
4. If it says "not recognised", add it to your PATH
5. In the terminal, run 'ollama pull llama3.2'
6. Type in a question to confirm it is running. Type '/bye' to exit it
7. Install the Python library by running 'pip install ollama'
8. Run the pipeline by running this commands: 'cd src/retrieval' and then 'python rag_system.py'.

### Multilingual Prototype Setup

The multilingual prototype uses three local models:

- `BAAI/bge-m3` - multilingual retrieval (~2.2 GB)
- `qwen2.5:3b-instruct` - passage selection and grounded answer generation (1.9 GB)
- `facebook/nllb-200-distilled-600M` - multilingual translation (~2.5 GB)

Total first-time model download is approximately 6.5-7 GB.

#### 1. Install project dependencies

From the project root:

1. 'pip install -r requirements.txt'

2. Download qwen2.5 : run 'ollama pull qwen2.5:3b-instruct'

3. Download BGE-M3 and NLLB : run 'python src/retrieval/multilingual_test.py'
--> BGE-M3 and NLLB are downloaded automatically from Hugging Face when the multilingual test is run for the first time

**The downloaded models are cached locally and do not need to be downloaded again for later runs.**