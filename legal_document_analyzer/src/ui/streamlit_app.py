
import streamlit as st
from ..ingestion.document_loader import load_text
from ..preprocessing.text_cleaner import normalize
from ..preprocessing.section_splitter import split_into_sections
from ..nlp.clause_extractor import extract_clauses
from ..summarization.abstractive import summarize as abs_sum
from ..risk.risk_analyzer import analyze as risk_analyze
from ..output.report_builder import to_json, to_markdown, to_docx

st.set_page_config(page_title='Legal Document Analyzer', layout='wide')

st.title('📑 Legal Document Analyzer')

uploaded = st.file_uploader('Upload a contract (PDF/DOCX/TXT)', type=['pdf','docx','txt'])
if uploaded:
    tmp = f'/tmp/{uploaded.name}'
    with open(tmp, 'wb') as f:
        f.write(uploaded.read())
    doc = load_text(tmp)
    text = normalize(doc['text'])
    sections = split_into_sections(text)
    clauses = extract_clauses(sections)
    summary = abs_sum(text)
    risk = risk_analyze(clauses)

    st.subheader('Summary')
    st.write(summary)

    st.subheader('Extracted Clauses')
    for cl in clauses:
        with st.expander(f"{cl['type'].replace('_',' ').title()} ({cl['section']})"):
            st.write(cl['text'])

    st.subheader('Risk Analysis')
    st.metric('Risk Score', risk['score'], help=f"{risk['level'].upper()} risk")
    for f in risk.get('findings', []):
        st.write(f"• {f['clause_type'].title()} → " + ', '.join([r['rule'] for r in f['risks']]))

    outdir = st.text_input('Output directory', 'outputs')
    if st.button('Save Report'):
        to_json(outdir, {'summary': summary, 'clauses': clauses, 'risk': risk})
        to_markdown(outdir, summary, clauses, risk)
        to_docx(outdir, summary, clauses, risk)
        st.success(f'Report saved to {outdir}')
