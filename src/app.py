
from fastapi import FastAPI, UploadFile, File
from typing import Dict

from ..ingestion.document_loader import load_text
from ..preprocessing.text_cleaner import normalize
from ..preprocessing.section_splitter import split_into_sections
from ..nlp.clause_extractor import extract_clauses
from ..summarization.extractive import summarize as ext_sum
from ..summarization.abstractive import summarize as abs_sum
from ..risk.risk_analyzer import analyze as risk_analyze

app = FastAPI(title='Legal Document Analyzer API')

@app.post('/analyze')
async def analyze(file: UploadFile = File(...)) -> Dict:
    content = await file.read()
    tmp = f'/tmp/{file.filename}'
    with open(tmp, 'wb') as f:
        f.write(content)
    doc = load_text(tmp)
    text = normalize(doc['text'])
    sections = split_into_sections(text)
    clauses = extract_clauses(sections)
    summary = abs_sum(text)
    risk = risk_analyze(clauses)
    return {'summary': summary, 'clauses': clauses, 'risk': risk, 'meta': doc.get('meta', {})}
