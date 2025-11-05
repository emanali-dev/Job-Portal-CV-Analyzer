# simple, robust string matcher implementations
import time

def brute_force(cv_text, keywords):
    start = time.time()
    comparisons = 0
    matched = []
    missing = []
    text_lower = cv_text.lower()
    for kw in keywords:
        kw = kw.strip()
        if not kw:
            missing.append(kw); continue
        kw_lower = kw.lower()
        found = False
        for i in range(len(text_lower) - len(kw_lower) + 1):
            comparisons += 1
            if text_lower[i:i+len(kw_lower)] == kw_lower:
                matched.append(kw)
                found = True
                break
        if not found:
            missing.append(kw)
    elapsed = time.time() - start
    relevance = (len(matched) / len(keywords) * 100) if keywords else 0
    return {"matched": matched, "missing": missing, "comparisons": comparisons, "time": elapsed, "relevance": round(relevance,2)}


def kmp_search(cv_text, keywords):
    start = time.time()
    comparisons = 0
    matched = []
    missing = []
    text = cv_text.lower()

    def compute_lps(pat):
        lps = [0]*len(pat)
        length = 0
        i = 1
        while i < len(pat):
            if pat[i] == pat[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length-1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    for kw in keywords:
        kw = kw.strip()
        if not kw:
            missing.append(kw); continue
        pat = kw.lower()
        M = len(pat); N = len(text)
        lps = compute_lps(pat)
        i = j = 0
        found = False
        while i < N:
            comparisons += 1
            if pat[j] == text[i]:
                i += 1; j += 1
                if j == M:
                    matched.append(kw)
                    found = True
                    break
            else:
                if j != 0:
                    j = lps[j-1]
                else:
                    i += 1
        if not found:
            missing.append(kw)
    elapsed = time.time() - start
    relevance = (len(matched) / len(keywords) * 100) if keywords else 0
    return {"matched": matched, "missing": missing, "comparisons": comparisons, "time": elapsed, "relevance": round(relevance,2)}


def rabin_karp(cv_text, keywords, prime=101):
    start = time.time()
    comparisons = 0
    matched = []
    missing = []
    text = cv_text.lower()
    d = 256
    for kw in keywords:
        kw = kw.strip()
        if not kw:
            missing.append(kw); continue
        M = len(kw); N = len(text)
        pat = kw.lower()
        h = pow(d, M-1) % prime
        p_hash = 0
        t_hash = 0
        for i in range(M):
            p_hash = (d*p_hash + ord(pat[i])) % prime
            if i < N:
                t_hash = (d*t_hash + ord(text[i])) % prime
        found = False
        for i in range(N - M + 1):
            comparisons += 1
            if p_hash == t_hash and text[i:i+M] == pat:
                matched.append(kw)
                found = True
                break
            if i < N-M:
                t_hash = (d*(t_hash - ord(text[i]) * h) + ord(text[i+M])) % prime
                t_hash = (t_hash + prime) % prime
        if not found:
            missing.append(kw)
    elapsed = time.time() - start
    relevance = (len(matched) / len(keywords) * 100) if keywords else 0
    return {"matched": matched, "missing": missing, "comparisons": comparisons, "time": elapsed, "relevance": round(relevance,2)}
