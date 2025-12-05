
import re

CLAUSE_REGEX = {
    'termination': re.compile(r'termination|term|end date', re.I),
    'confidentiality': re.compile(r'confidential|non\-disclosure|nda|confidential information', re.I),
    'indemnification': re.compile(r'indemnif\w*|hold harmless', re.I),
    'limitation_of_liability': re.compile(r'limit(ation)? of liability|liability cap|consequential damages', re.I),
    'payment_terms': re.compile(r'payment|invoice|net\s*\d+|fees?', re.I),
    'governing_law': re.compile(r'governing law|jurisdiction|venue', re.I),
    'dispute_resolution': re.compile(r'arbitration|dispute resolution|mediati(on|e)', re.I),
    'ip_ownership': re.compile(r'intellectual property|ownership|license', re.I),
    'force_majeure': re.compile(r'force majeure|unforeseen events', re.I),
    'assignment': re.compile(r'assignment|transfer|delegation', re.I),
    'data_protection': re.compile(r'data protection|privacy|gdpr|personal data', re.I),
}
