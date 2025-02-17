import numpy as np
import matplotlib.pyplot as plt


# Define the betting simulation function
def simulate_game(strategy, initial_amount=100, num_bets=100, num_simulations=100):
    results = []
    for _ in range(num_simulations):
        balance = initial_amount
        for _ in range(1, num_bets + 1):
            if balance <= 0:
                break
            # Determine the betting percentage based on strategy
            bet_fraction = strategies[strategy]

            bet_amount = bet_fraction * balance
            outcome = np.random.choice(["win", "lose"], p=[0.5, 0.5])
            if outcome == "win":
                balance += 3 * bet_amount  # Win gives 3x the bet amount
            else:
                balance -= bet_amount  # Lose means losing the bet amount

        results.append(balance)
    return results


# Define strategies and simulate games
strategies = {
    "10%": 0.10,
    "5%": 0.05,
    "15%": 0.15,
    "20%": 0.20,
    "30%": 0.3,
    "40%": 0.4,
    "70%": 0.7,
}


num_simulations = 100
all_results = {}

for strategy in strategies:
    all_results[strategy] = simulate_game(strategy, num_simulations=num_simulations)

# Plot the results
plt.figure(figsize=(12, 6))
plt.boxplot(
    [all_results[strategy] for strategy in strategies],
    labels=strategies,
    patch_artist=True,
    showfliers=False,
)
plt.title("Distribution of Final Balances for Different Betting Strategies")
plt.ylabel("Final Balance ($)")
plt.xlabel("Betting Strategy")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()
