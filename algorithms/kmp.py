def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i].lower() == pattern[length].lower():
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    i = j = 0
    positions = []
    comparisons = 0
    
    while i < n:
        comparisons += 1
        if text[i].lower() == pattern[j].lower():
            i += 1
            j += 1
        if j == m:
            positions.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i].lower() != pattern[j].lower():
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return positions, comparisons
