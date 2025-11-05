def brute_force_search(text, pattern):
    n, m = len(text), len(pattern)
    positions = []
    comparisons = 0
    
    for i in range(n - m + 1):
        match = True
        for j in range(m):
            comparisons += 1
            if text[i + j].lower() != pattern[j].lower():
                match = False
                break
        if match:
            positions.append(i)
    
    return positions, comparisons
