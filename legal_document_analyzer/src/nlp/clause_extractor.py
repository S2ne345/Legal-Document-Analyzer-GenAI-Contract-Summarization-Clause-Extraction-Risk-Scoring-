
from typing import List, Dict
from .clause_patterns import CLAUSE_REGEX


def extract_clauses(sections: List[Dict]) -> List[Dict]:
    extracted = []
    for sec in sections:
        text = sec.get('text', '')
        for name, rx in CLAUSE_REGEX.items():
            if rx.search(text):
                extracted.append({
                    'type': name,
                    'section': sec.get('title', ''),
                    'text': text
                })
    return extracted
