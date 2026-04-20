import streamlit as st
import tempfile
import os
from loaders import load_file
from splitters import split_chunks
from clause_detection import analyze_chunks, check_required_clauses
from llm import explain_all_flags

st.set_page_config(page_title="Contract Analyzer", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');

* { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'DM Serif Display', serif; }

.stApp { background-color: #0f0f0f; color: #e8e0d0; }

section[data-testid="stSidebar"] { background-color: #1a1a1a; border-right: 1px solid #2a2a2a; }

.main-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    color: #e8e0d0;
    border-bottom: 2px solid #c9a96e;
    padding-bottom: 0.5rem;
    margin-bottom: 0.2rem;
}
.subtitle {
    color: #888;
    font-size: 0.95rem;
    margin-bottom: 2rem;
    font-weight: 300;
}
.section-header {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    color: #c9a96e;
    margin: 1.5rem 0 0.8rem 0;
    border-left: 3px solid #c9a96e;
    padding-left: 0.8rem;
}
.found-badge {
    display: inline-block;
    background: #1a3a2a;
    color: #4caf7d;
    border: 1px solid #4caf7d;
    border-radius: 4px;
    padding: 4px 12px;
    margin: 3px;
    font-size: 0.82rem;
    font-weight: 500;
}
.missing-badge {
    display: inline-block;
    background: #3a1a1a;
    color: #e05555;
    border: 1px solid #e05555;
    border-radius: 4px;
    padding: 4px 12px;
    margin: 3px;
    font-size: 0.82rem;
    font-weight: 500;
}
.risk-card {
    background: #1c1510;
    border: 1px solid #8b4513;
    border-left: 4px solid #e07020;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
}
.ambiguous-card {
    background: #141520;
    border: 1px solid #3a3a8b;
    border-left: 4px solid #6070e0;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
}
.phrase-tag {
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    color: #c9a96e;
}
.context-text {
    color: #999;
    font-size: 0.82rem;
    margin-top: 0.4rem;
    font-style: italic;
    line-height: 1.5;
}
.ai-box {
    background: #141a14;
    border: 1px solid #2a4a2a;
    border-radius: 8px;
    padding: 1.5rem;
    color: #b8d4b8;
    font-size: 0.9rem;
    line-height: 1.8;
    white-space: pre-wrap;
}
.stat-box {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
}
.stat-number { font-size: 2rem; font-weight: 700; font-family: 'DM Serif Display', serif; }
.stat-label { font-size: 0.75rem; color: #888; text-transform: uppercase; letter-spacing: 0.05em; }
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-title">⚖️ Contract Risk Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload a contract to detect missing clauses, risky language, and ambiguous terms.</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Contract", type=["pdf", "docx", "txt"], label_visibility="collapsed")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with st.spinner("Analyzing contract..."):
        docs = load_file(tmp_path)
        chunks = split_chunks(docs)
        checklist_result = check_required_clauses(tmp_path)
        final_result = analyze_chunks(chunks, checklist_result)
        ai_output = explain_all_flags(final_result)

    os.unlink(tmp_path)

    checklist = ai_output['clause_checklist']
    risk_flags = ai_output['risk_flags']
    ambiguity_flags = ai_output['ambiguity_flags']

    # stats row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="stat-box"><div class="stat-number" style="color:#4caf7d">{len(checklist["found"])}</div><div class="stat-label">Clauses Found</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-box"><div class="stat-number" style="color:#e05555">{len(checklist["missing"])}</div><div class="stat-label">Clauses Missing</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-box"><div class="stat-number" style="color:#e07020">{len(risk_flags)}</div><div class="stat-label">Risk Flags</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="stat-box"><div class="stat-number" style="color:#6070e0">{len(ambiguity_flags)}</div><div class="stat-label">Ambiguous Terms</div></div>', unsafe_allow_html=True)

    st.markdown("")

    left, right = st.columns([1, 1], gap="large")

    with left:
        # clause checklist
        st.markdown('<div class="section-header">Clause Checklist</div>', unsafe_allow_html=True)
        st.markdown("**✅ Found**")
        found_html = "".join([f'<span class="found-badge">✓ {c}</span>' for c in checklist["found"]])
        st.markdown(found_html, unsafe_allow_html=True)

        st.markdown("**❌ Missing**")
        missing_html = "".join([f'<span class="missing-badge">✗ {c}</span>' for c in checklist["missing"]])
        st.markdown(missing_html, unsafe_allow_html=True)

        # risky phrases
        st.markdown('<div class="section-header">⚠️ Risky Language</div>', unsafe_allow_html=True)
        if risk_flags:
            seen = set()
            for flag in risk_flags:
                if flag['phrase'] not in seen:
                    seen.add(flag['phrase'])
                    st.markdown(f'''<div class="risk-card">
                        <div class="phrase-tag">🔴 {flag["phrase"]}</div>
                        <div class="context-text">{flag["context"][:200]}...</div>
                    </div>''', unsafe_allow_html=True)
        else:
            st.markdown("No risky language detected.")

        # ambiguous terms
        st.markdown('<div class="section-header">🔵 Ambiguous Terms</div>', unsafe_allow_html=True)
        if ambiguity_flags:
            seen = set()
            for flag in ambiguity_flags:
                if flag['phrase'] not in seen:
                    seen.add(flag['phrase'])
                    st.markdown(f'''<div class="ambiguous-card">
                        <div class="phrase-tag">🔵 {flag["phrase"]}</div>
                        <div class="context-text">{flag["context"][:200]}...</div>
                    </div>''', unsafe_allow_html=True)
        else:
            st.markdown("No ambiguous terms detected.")

    with right:
        st.markdown('<div class="section-header">🤖 AI Analysis</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ai-box">{ai_output.get("ai_explanation", "No AI explanation available.")}</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align:center; padding: 4rem 2rem; color: #555;">
        <div style="font-size: 3rem;">📄</div>
        <div style="font-family: DM Serif Display; font-size: 1.2rem; margin-top: 1rem; color: #777;">Drop a contract to get started</div>
        <div style="font-size: 0.85rem; margin-top: 0.5rem;">Supports PDF, DOCX, and TXT</div>
    </div>
    """, unsafe_allow_html=True)