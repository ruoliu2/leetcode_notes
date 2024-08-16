def sieve(n):
    primes = []
    is_prime = [1] * (n + 1)
    for i in range(2, n + 1):
        if not is_prime[i]:
            continue
        primes.append(i)
        for j in range(i * i, n + 1, i):
            is_prime[j] = 0
    return primes
