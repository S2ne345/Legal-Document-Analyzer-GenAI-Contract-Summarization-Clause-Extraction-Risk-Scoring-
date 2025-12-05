
import re
from typing import List, Dict

HEADING_PATTERN = re.compile(r'^(\d+(?:\.\d+)*)\s+[A-Z][A-Za-z\s\-]+$')


def split_into_sections(text: str) -> List[Dict]:
    lines = text.split('
')
    sections = []
    current = {'title': 'Preamble', 'content': []}
    for ln in lines:
        if HEADING_PATTERN.match(ln.strip()):
            # Start new section
            sections.append(current)
            current = {'title': ln.strip(), 'content': []}
        else:
            current['content'].append(ln)
    sections.append(current)
    # Join content
    for s in sections:
        s['text'] = '
'.join(s['content']).strip()
        del s['content']
    return sections
