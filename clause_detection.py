import re
from loaders import load_file
from splitters import split_chunks


REQUIRED_CLAUSES = [
    "confidentiality", "termination", "dispute resolution", "indemnity",
    "payment terms", "governing law", "limitation of liability",
    "force majeure", "service level agreement", "SLA",
    "data protection", "GDPR", "DPDP"
]

RISKY_PHRASES = [
    "termination without cause", "termination without notice", "indemnify fully",
    "penalty at discretion", "sole discretion", "without liability", "waives all rights",
    "without any prior notice", "without prior notice", "at its sole discretion",
    "no warranties", "makes no warranties", "at sole risk",
    "without sufficient reason", "detrimental to", "either party alone",
    "by written notice"
]

AMBIGUOUS_TERMS = [
    "reasonable time", "as needed", "at discretion", "may or may not",
    "best efforts", "satisfactory performance",
    "reasonable period", "reasonably required", "from time to time",
    "deemed appropriate", "deemed necessary", "as deemed",
    "considered reasonable", "considered fair", "fair and appropriate",
    "without sufficient reason", "resolved amicably", "amicably between"
]

def check_required_clauses(file_name):
 full_text=load_file(file_name)
 full_text=" ".join([doc.page_content for doc in full_text])
 found=[]
 missing=[]

 for clause in REQUIRED_CLAUSES:
  pattern=re.compile(r'\b'+re.escape(clause)+r'\b',re.IGNORECASE)
  if pattern.search(full_text):
   found.append(clause)
  else:
   missing.append(clause)

 return {"found":found,"missing":missing}


def check_risky_phrases(chunks):
    flags = []
    seen = set()

    for chunk in chunks:
        for phrase in RISKY_PHRASES:
            pattern = re.compile(r'\b' + re.escape(phrase) + r'\b', re.IGNORECASE)
            if pattern.search(chunk.page_content):
                key = (chunk.page_content[:100], phrase)
                if key not in seen:
                    seen.add(key)
                    flags.append({
                        "type": "Risky",
                        "phrase": phrase,
                        "context": chunk.page_content
                    })

    return flags

def check_ambiguous_terms(chunks):
    flags = []
    seen = set()

    for chunk in chunks:
        for phrase in AMBIGUOUS_TERMS:
            pattern = re.compile(r'\b' + re.escape(phrase) + r'\b', re.IGNORECASE)
            if pattern.search(chunk.page_content):
                key = (chunk.page_content[:100], phrase)
                if key not in seen:
                    seen.add(key)
                    flags.append({
                        "type": "ambiguous",
                        "phrase": phrase,
                        "context": chunk.page_content
                    })

    return flags
    
checklist_result=check_required_clauses("SampleBusinessContract.docx")

def analyze_chunks(chunks,checklist_result):
 return {
        "clause_checklist": checklist_result,
        "risk_flags": check_risky_phrases(chunks),
        "ambiguity_flags": check_ambiguous_terms(chunks)
    }

docs=load_file("SampleBusinessContract.docx")
chunk_split=split_chunks(docs)
#final_result=analyze_chunks(chunk_split,checklist_result)