# SIG
def solution(blocks, writers, threshold):
    tmp, res = [], []
    delta = [0] * blocks  # could using treeMap to avoid sparse representation
    for s, e in writers:
        delta[s] += 1
        delta[e+1] -= 1
    preSum = 0
    for i in range(blocks):
        preSum += delta[i]
        if preSum >= threshold:
            tmp.append(i)
    # get range [start, end] format store in res
    # 1 2 3 5 6 7 => [1, 3], [5, 7]
    start, end = 0, 0
    for i, val in enumerate(tmp):
        if i == 0:
            start = val
            end = val
        elif val == tmp[i-1] + 1:
            end = val
        else:
            res.append([start, end])
            start = val
            end = val
    res.append([start, end])
    return res
