import os
from dotenv import load_dotenv
from groq import Groq
from clause_detection import analyze_chunks,checklist_result
from loaders import load_file
from splitters import split_chunks

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def explain_all_flags(analysis_result):
    all_flags = analysis_result['risk_flags'] + analysis_result['ambiguity_flags']
    missing = analysis_result['clause_checklist']['missing']

    flags_text = ""
    for i, flag in enumerate(all_flags):
        flags_text += f"\nFlag {i+1}: Type: {flag['type']} | Phrase: '{flag['phrase']}' | Context: {flag['context']}\n"

    prompt = f"""
    You are an expert legal contract analyst with decades of experience.
    
    Analyze the following flagged clauses and missing clauses from a service agreement.
    
    FLAGGED CLAUSES:
    {flags_text}
    
    MISSING CLAUSES:
    {', '.join(missing)}
    
    For each flagged clause, explain in 2 sentences why it is risky or ambiguous for the client.
    For each missing clause, explain in 1 sentence why its absence is a problem.
    
    Format exactly like this:
    FLAG 1: explanation
    FLAG 2: explanation
    MISSING - clause name: explanation
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    analysis_result['ai_explanation'] = response.choices[0].message.content
    return analysis_result

docs=load_file("SampleBusinessContract.docx")
chunk_split=split_chunks(docs)
final_result=analyze_chunks(chunk_split,checklist_result)
if __name__ == "__main__":
    ai_output=explain_all_flags(final_result)
#print(ai_output)
