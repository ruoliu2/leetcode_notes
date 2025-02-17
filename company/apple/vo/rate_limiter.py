import time
from collections import defaultdict, deque
from datetime import datetime, timedelta


class RateLimiter:
    def __init__(self, limit=10, time_window=15):
        self.limit = limit  # Max allowed requests
        self.time_window = timedelta(minutes=time_window)  # Time window in minutes
        self.ip_requests = defaultdict(
            deque
        )  # Dictionary to track IP request times using deque

    def is_allowed(self, ip):
        # Current time
        now = datetime.now()

        # Remove old timestamps (outside the time window)
        while self.ip_requests[ip] and now - self.ip_requests[ip][0] > self.time_window:
            self.ip_requests[ip].popleft()  # Fast removal of the oldest entry

        # Check if the IP exceeded the limit
        if len(self.ip_requests[ip]) >= self.limit:
            return False

        # If not, allow the access and add the current timestamp
        self.ip_requests[ip].append(now)
        return True


# Example Usage
if __name__ == "__main__":
    rate_limiter = RateLimiter(limit=10, time_window=15)

    # Test IP accesses
    test_ips = ["192.168.0.1", "192.168.0.2"]

    for i in range(12):
        ip = test_ips[0] if i < 6 else test_ips[1]  # First 6 accesses from one IP
        print(f"IP {ip} access allowed: {rate_limiter.is_allowed(ip)}")
        time.sleep(1)  # Simulating 1 second between accesses
