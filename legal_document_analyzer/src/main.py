
import argparse
from pathlib import Path

from .ingestion.document_loader import load_text
from .preprocessing.text_cleaner import normalize
from .preprocessing.section_splitter import split_into_sections
from .nlp.clause_extractor import extract_clauses
from .summarization.abstractive import summarize as abs_sum
from .risk.risk_analyzer import analyze as risk_analyze
from .output.report_builder import to_json, to_markdown, to_docx


def run(input_path: str, outdir: str):
    doc = load_text(input_path)
    text = normalize(doc['text'])
    sections = split_into_sections(text)
    clauses = extract_clauses(sections)
    summary = abs_sum(text)
    risk = risk_analyze(clauses)
    data = {'summary': summary, 'clauses': clauses, 'risk': risk, 'meta': doc.get('meta', {})}
    Path(outdir).mkdir(parents=True, exist_ok=True)
    to_json(outdir, data)
    to_markdown(outdir, summary, clauses, risk)
    to_docx(outdir, summary, clauses, risk)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Legal Document Analyzer CLI')
    parser.add_argument('--input', required=True, help='Path to contract file (PDF/DOCX/TXT)')
    parser.add_argument('--outdir', default='outputs', help='Directory to write reports')
    args = parser.parse_args()
    run(args.input, args.outdir)
