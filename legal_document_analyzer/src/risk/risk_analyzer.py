
import json
import re
from pathlib import Path
from typing import List, Dict

from ..config import CONFIG

RULES_PATH = Path(__file__).with_name('risk_rules.json')
RULES = json.loads(RULES_PATH.read_text(encoding='utf-8'))

WEIGHTS = CONFIG.get('risk', 'weights', default={})


def analyze(clauses: List[Dict]) -> Dict:
    findings = []
    total_score = 0
    for cl in clauses:
        text = cl.get('text', '')
        risk_hits = []
        for key, rule in RULES.items():
            rx = re.compile(rule['pattern'])
            if rx.search(text):
                weight = WEIGHTS.get(key, 10)
                risk_hits.append({'rule': key, 'weight': weight})
                total_score += weight
        if risk_hits:
            findings.append({
                'clause_type': cl.get('type'),
                'section': cl.get('section'),
                'risks': risk_hits
            })
    thresholds = CONFIG.get('risk', 'thresholds', default={'high':70,'medium':40})
    level = 'low'
    if total_score >= thresholds['high']:
        level = 'high'
    elif total_score >= thresholds['medium']:
        level = 'medium'
    return {'score': total_score, 'level': level, 'findings': findings}
