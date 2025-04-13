import bisect


class Account:
    def __init__(self):
        # Sorted list of (timestamp, delta) for balance events.
        self.events = []
        # Sorted list of (timestamp, amount) for transfer-out spending events.
        self.spending_events = []
        # Scheduled payments: paymentId -> (scheduled_time, amount)
        # for time optimized, we can use sortedDict scheduled_time -> [(paymentId, amount)]
        # get items and sum until the timeAt
        # here we use a dict for simplicity
        self.scheduled_payments = {}

    def add_event(self, timestamp, delta):
        # Insert event while keeping the list sorted.
        bisect.insort(self.events, (timestamp, delta))

    def add_spending(self, timestamp, amount):
        bisect.insort(self.spending_events, (timestamp, amount))

    def cumulative_sum(self, timeAt):
        # Sum all events with timestamp <= timeAt.
        idx = bisect.bisect_right(self.events, (timeAt, float("inf")))
        return sum(delta for (ts, delta) in self.events[:idx])

    def cumulative_spending(self, timeAt):
        # Sum spending events (i.e. transfer-out amounts) up to timeAt.
        idx = bisect.bisect_right(self.spending_events, (timeAt, float("inf")))
        return sum(amount for (ts, amount) in self.spending_events[:idx])

    def scheduled_payments_sum(self, timeAt):
        # Sum scheduled payment amounts that are due by timeAt.
        total = 0
        for sched_time, amount in self.scheduled_payments.values():
            if sched_time <= timeAt:
                total += amount
        return total

    def _merge_sorted_lists(self, list1, list2):
        """Helper method to merge two sorted lists using two-pointer approach."""
        merged = []
        i, j = 0, 0
        while i < len(list1) and j < len(list2):
            if list1[i] <= list2[j]:
                merged.append(list1[i])
                i += 1
            else:
                merged.append(list2[j])
                j += 1
        # Add remaining elements
        merged.extend(list1[i:])
        merged.extend(list2[j:])
        return merged

    def merge(self, other):
        # Merge events and spending events using the helper method
        self.events = self._merge_sorted_lists(self.events, other.events)
        self.spending_events = self._merge_sorted_lists(
            self.spending_events, other.spending_events
        )
        # Merge scheduled payments
        self.scheduled_payments.update(other.scheduled_payments)


class BankSystem:
    def __init__(self):
        self.accounts = {}  # accountId -> Account
        self.payment_counter = 0  # Global payment id generator

    def get_account(self, accountId):
        if accountId not in self.accounts:
            self.accounts[accountId] = Account()
        return self.accounts[accountId]

    def CreateAccount(self, timestamp, accountId):
        if accountId in self.accounts:
            # Account already exists; you could also raise an exception.
            return
        self.accounts[accountId] = Account()

    def Deposit(self, timestamp, accountId, amount):
        account = self.get_account(accountId)
        account.add_event(timestamp, amount)

    def Transfer(self, timestamp, fromAccountId, toAccountId, amount):
        from_account = self.get_account(fromAccountId)
        to_account = self.get_account(toAccountId)
        # Deduct amount from sender and record spending.
        from_account.add_event(timestamp, -amount)
        from_account.add_spending(timestamp, amount)
        # Add amount to recipient.
        to_account.add_event(timestamp, amount)

    def TopSpenders(self, timestamp, n):
        # Get cumulative spending for each account up to timestamp.
        spendings = []
        for accountId, account in self.accounts.items():
            spend = account.cumulative_spending(timestamp)
            spendings.append((spend, accountId))
        # Sort descending by spending and then by accountId for tie-breaking.
        spendings.sort(key=lambda x: (-x[0], x[1]))
        # Format result as "accountId(spendAmount)".
        result = []
        for i in range(min(n, len(spendings))):
            spend, accountId = spendings[i]
            result.append(f"{accountId}({spend})")
        return result

    def SchedulePayment(self, timestamp, accountId, amount, delay):
        account = self.get_account(accountId)
        scheduled_time = timestamp + delay
        self.payment_counter += 1
        paymentId = self.payment_counter
        account.scheduled_payments[paymentId] = (scheduled_time, amount)
        return paymentId

    def CancelPayment(self, timestamp, accountId, paymentId):
        account = self.get_account(accountId)
        if paymentId in account.scheduled_payments:
            del account.scheduled_payments[paymentId]
            return paymentId
        return None

    def GetBalance(self, timestamp, accountId, timeAt):
        account = self.get_account(accountId)
        # Base balance from deposits/transfers.
        base_balance = account.cumulative_sum(timeAt)
        # Subtract scheduled payments that are due.
        scheduled_out = account.scheduled_payments_sum(timeAt)
        return base_balance - scheduled_out

    def MergeAccount(self, timestamp, accountId1, accountId2):
        account1 = self.get_account(accountId1)
        account2 = self.get_account(accountId2)
        # Merge account2's data into account1.
        account1.merge(account2)
        # Remove account2 from the system.
        del self.accounts[accountId2]


# Example usage:
if __name__ == "__main__":
    bank = BankSystem()
    bank.CreateAccount(1, "A1")
    bank.CreateAccount(1, "A2")
    bank.Deposit(2, "A1", 1000)
    bank.Deposit(2, "A2", 500)
    bank.Transfer(3, "A1", "A2", 200)
    payment_id = bank.SchedulePayment(4, "A1", 100, 5)  # Scheduled at time 9
    print(
        "Balance A1 at time 3:", bank.GetBalance(4, "A1", 3)
    )  # Before scheduled payment
    print(
        "Balance A1 at time 10:", bank.GetBalance(4, "A1", 10)
    )  # After scheduled payment
    top = bank.TopSpenders(10, 2)
    print("Top spenders at time 10:", top)
    bank.MergeAccount(11, "A1", "A2")
    print("Merged Balance A1 at time 10:", bank.GetBalance(11, "A1", 10))
