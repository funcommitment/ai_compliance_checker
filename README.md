# ⚖️ AI Contract Risk Analyzer

A local AI-powered tool that analyzes legal contracts for missing clauses, 
risky language, and ambiguous terms using regex-based detection and 
LLM-powered explanations.

## What It Does

- Detects 13 standard legal clauses and flags which are missing
- Identifies risky phrases that create legal exposure for the client
- Flags ambiguous terms that lack clear definitions or criteria
- Generates plain-English explanations for every flag using Llama 3.3 70B via Groq

## Tech Stack

- Python 3.12
- Streamlit — UI
- LangChain — document loading and text splitting
- Groq API (Llama-3.3-70b-versatile) — AI explanations
- Regex — clause and phrase detection

## Project Structure
ai_compliance_checker/
├── app.py               # Streamlit UI
├── loaders.py           # PDF, DOCX, TXT document loading
├── splitters.py         # Text chunking with overlap
├── clause_detection.py  # Regex-based detection logic
├── llm.py              # Groq API integration
├── .env.example         # Environment variable template
├── SampleBusinessContract.docx  # Test contract
└── requirements.txt

## Setup

```bash
git clone https://github.com/funcommitment/ai_compliance_checker
cd ai_compliance_checker
pip install -r requirements.txt
```

Create a `.env` file:
GROQ_API_KEY=your_api_key_here

Run:
```bash
streamlit run app.py
```

## Supported Formats

PDF, DOCX, TXT

## How It Works

1. Document is loaded and split into overlapping chunks
2. Required clauses are checked against full text via regex
3. Risky phrases and ambiguous terms are matched across chunks
4. All flags are sent to Llama 3.3 70B for plain-English explanation

## Known Limitations

- Clause detection is keyword-based — semantic variations may be missed
- Keyword lists are tuned for service agreements; other contract types 
  may need different phrase sets
- No evaluation framework against labeled contract datasets

## Sample Output

Tested against a deliberately constructed service agreement with known 
issues — detected 9/9 missing clauses, 9/10 risky phrases, 
8/8 ambiguous terms.
