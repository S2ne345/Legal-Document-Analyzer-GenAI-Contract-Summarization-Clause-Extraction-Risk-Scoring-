
import re
from typing import List


def normalize(text: str) -> str:
    # Normalize whitespace and fix hyphenation across line breaks
    t = re.sub(r'', '', text)
    t = re.sub(r'[	 ]+', ' ', t)
    t = re.sub(r'\s+
', '
', t)
    t = re.sub(r'
{2,}', '

', t)
    # Fix broken words due to hyphenation at EOL
    t = re.sub(r'(\w+)-
(\w+)', r'
', t)
    return t.strip()


def strip_headers_footers(lines: List[str]) -> List[str]:
    cleaned = []
    for ln in lines:
        if re.search(r'Page\s+\d+|Confidential|Draft', ln, re.I):
            continue
        cleaned.append(ln)
    return cleaned
