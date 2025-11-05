def rabin_karp_search(text, pattern, prime=101):
    n, m = len(text), len(pattern)
    d = 256
    hpattern = 0
    htext = 0
    h = 1
    positions = []
    comparisons = 0

    for i in range(m - 1):
        h = (h * d) % prime

    for i in range(m):
        hpattern = (d * hpattern + ord(pattern[i].lower())) % prime
        htext = (d * htext + ord(text[i].lower())) % prime

    for i in range(n - m + 1):
        if hpattern == htext:
            match = True
            for j in range(m):
                comparisons += 1
                if text[i + j].lower() != pattern[j].lower():
                    match = False
                    break
            if match:
                positions.append(i)
        if i < n - m:
            htext = (d * (htext - ord(text[i].lower()) * h) + ord(text[i + m].lower())) % prime
            if htext < 0:
                htext += prime

    return positions, comparisons
