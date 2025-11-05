import os

JOB_DESC_DIR = "job_descriptions"

def load_keywords_for_role(role):
    """
    role: filename without extension, e.g., 'data_scientist'
    returns list of keywords or [] if not found
    """
    path = os.path.join(JOB_DESC_DIR, f"{role}.txt")
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        txt = f.read().strip()
    # split by comma and strip
    keywords = [k.strip() for k in txt.split(',') if k.strip()]
    return keywords
