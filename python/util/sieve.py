def sieve(n):
    prime = [1] * (n + 1)
    p = 2
    while p * p <= n:  # if prime[p] unchanged, then its prime
        if prime[p] == 1:  # update all multiples of p
            for i in range(p * p, n + 1, p):
                prime[i] = 0
        p += 1

    # return all primes
    return [p for p in range(2, n) if prime[p] == 1]
