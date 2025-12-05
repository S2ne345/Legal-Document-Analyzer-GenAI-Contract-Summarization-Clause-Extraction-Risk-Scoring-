
# Legal Document Analyzer (GenAI)

A Python-based system to **summarize legal documents** and **extract key clauses** with **risk analysis**. It supports PDFs, DOCX, and TXT, provides extractive and (optional) abstractive summaries, and produces structured outputs.

## Features
- Document ingestion (PDF/DOCX/TXT + optional OCR)
- Text preprocessing & section splitting
- Clause extraction (termination, confidentiality, indemnification, payment terms, etc.)
- Summarization: TextRank (extractive) + optional transformers (abstractive)
- Simple RAG-style semantic search (TF–IDF + cosine)
- Risk analysis with configurable rules
- Report builder (JSON/CSV/Markdown/Word)
- FastAPI endpoints + Streamlit UI

## Quick Start
```bash
# (Recommended) Create a virtual environment
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run CLI analysis on a sample file
python src/main.py --input tests/sample_contracts/sample_contract_1.txt --outdir outputs

# Start API
uvicorn src.api.app:app --reload

# Launch UI
streamlit run src/ui/streamlit_app.py
```

> Note: Abstractive summarization and advanced NER require optional libraries (e.g., `transformers`, `spaCy`). The code gracefully falls back to extractive methods if these are not available.

## Project Layout
```
legal_document_analyzer/
├── README.md
├── requirements.txt
├── config.yaml
├── src/
│   ├── main.py
│   ├── config.py
│   ├── utils/
│   │   ├── file_utils.py
│   │   └── logging_utils.py
│   ├── ingestion/
│   │   ├── document_loader.py
│   │   └── ocr.py
│   ├── preprocessing/
│   │   ├── text_cleaner.py
│   │   └── section_splitter.py
│   ├── nlp/
│   │   ├── clause_patterns.py
│   │   └── clause_extractor.py
│   ├── summarization/
│   │   ├── extractive.py
│   │   └── abstractive.py
│   ├── rag/
│   │   └── retriever.py
│   ├── risk/
│   │   ├── risk_rules.json
│   │   └── risk_analyzer.py
│   ├── output/
│   │   └── report_builder.py
│   ├── api/
│   │   └── app.py
│   └── ui/
│       └── streamlit_app.py
├── tests/
│   ├── test_extractive.py
│   └── sample_contracts/
│       └── sample_contract_1.txt
└── data/
    └── policies/
        └── playbook.yaml
```
