def getLargestIndexLen(feat1, feat2):
    feat = sorted(zip(feat1, feat2), key=lambda a: (a[0], -a[1]))
    # lis on feat2
    sub = []
    for _, num in feat:
        i = bisect_left(sub, num)
        if i == len(sub):
            sub.append(num)
        else:
            sub[i] = num
    return len(sub)
