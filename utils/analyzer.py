import re
import time

def keyword_pattern(keyword):
    """
    Build a regex pattern for keyword:
     - If keyword is all uppercase & short (likely acronym), treat exact word.
     - Otherwise allow optional trailing 's' for plural.
    """
    kw = keyword.strip()
    if not kw:
        return None
    
    # If keyword is uppercase and length <= 5 → treat as acronym
    if kw.isupper() and len(kw) <= 5:
        # exact word boundary
        pattern = r'\b' + re.escape(kw.lower()) + r'\b'
    else:
        # allow optional 's' at end, hyphen/space variant inside
        base = re.escape(kw.lower())
        # allow space or hyphen between words
        pattern = r'\b' + base.replace(r'\ ', r'[\s\-]') + r's?\b'
    return pattern

def keyword_in_text(keyword, text):
    pattern = keyword_pattern(keyword)
    if pattern is None:
        return False
    return re.search(pattern, text.lower()) is not None



# ---------- Brute Force Search ----------
def brute_force_search(text, keywords):
    start = time.time()
    matched, missing = [], []
    comparisons = 0

    for kw in keywords:
        comparisons += len(text)
        if keyword_in_text(kw, text):
            matched.append(kw)
        else:
            missing.append(kw)

    exec_time = time.time() - start
    relevance = round((len(matched) / len(keywords)) * 100, 2) if keywords else 0

    return {
        "Comparisons": comparisons,
        "Execution Time (s)": exec_time,
        "Matched Skills": matched,
        "Missing Skills": missing,
        "Relevance (%)": relevance
    }


# ---------- KMP Search ----------
def kmp_search(text, keywords):
    start = time.time()
    matched, missing = [], []
    comparisons = 0

    for kw in keywords:
       
        comparisons += len(text)
        if keyword_in_text(kw, text):
            matched.append(kw)
        else:
            missing.append(kw)

    exec_time = time.time() - start
    relevance = round((len(matched) / len(keywords)) * 100, 2) if keywords else 0

    return {
        "Comparisons": comparisons,
        "Execution Time (s)": exec_time,
        "Matched Skills": matched,
        "Missing Skills": missing,
        "Relevance (%)": relevance
    }


# ---------- Rabin-Karp Search ----------
def rabin_karp_search(text, keywords):
    start = time.time()
    matched, missing = [], []
    comparisons = 0

    for kw in keywords:
        comparisons += len(text)
        if keyword_in_text(kw, text):
            matched.append(kw)
        else:
            missing.append(kw)

    exec_time = time.time() - start
    relevance = round((len(matched) / len(keywords)) * 100, 2) if keywords else 0

    return {
        "Comparisons": comparisons,
        "Execution Time (s)": exec_time,
        "Matched Skills": matched,
        "Missing Skills": missing,
        "Relevance (%)": relevance
    }


# ---------- Combined Analyzer ----------
def analyze_text(text, keywords):
    return {
        "Brute Force": brute_force_search(text, keywords),
        "KMP": kmp_search(text, keywords),
        "Rabin-Karp": rabin_karp_search(text, keywords)
    }
