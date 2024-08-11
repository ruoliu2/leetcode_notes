def sieve(n):
    prime = [1] * (n + 1)
    p = 2
    while p * p <= n:
        # if prime[p] is not changed, then it is a prime
        if prime[p] == 1:
            # update all multiples of p
            for i in range(p * p, n + 1, p):
                prime[i] = 0
        p += 1

    # Print all prime numbers
    for p in range(2, n + 1):
        if prime[p]:
            print(p)
