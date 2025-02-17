from collections import defaultdict


class Pizza:
    # Base prices
    BASE_PRICES = {"small": 8.00, "medium": 10.00, "large": 12.00}
    CRUST_PRICES = {"thin": 0.00, "thick": 2.00, "stuffed": 3.00}
    TOPPING_PRICE = 1.50  # Price per topping

    def __init__(self, size="medium", crust="thin"):
        self.size = size
        self.crust = crust
        self.toppings = defaultdict(int)  # Topping name as key, amount as value

    def add_topping(self, topping, amount=1):
        """Add a specified amount of a topping to the pizza."""
        if amount > 0:
            self.toppings[topping] += amount
        else:
            print("Amount to add must be positive.")

    def remove_topping(self, topping, amount=1):
        """Remove a specified amount of a topping from the pizza."""
        if self.toppings[topping] > 0:
            if amount >= self.toppings[topping]:
                self.toppings[topping] = 0
            else:
                self.toppings[topping] -= amount
        else:
            print(f"Topping {topping} is not on the pizza.")

    def change_size(self, size):
        """Change the size of the pizza."""
        if size in self.BASE_PRICES:
            self.size = size
        else:
            print(f"Invalid size. Choose from {list(self.BASE_PRICES.keys())}.")

    def change_crust(self, crust):
        """Change the crust type of the pizza."""
        if crust in self.CRUST_PRICES:
            self.crust = crust
        else:
            print(f"Invalid crust. Choose from {list(self.CRUST_PRICES.keys())}.")

    def calculate_price(self):
        """Calculate the total price of the pizza."""
        base_price = self.BASE_PRICES[self.size]
        crust_price = self.CRUST_PRICES[self.crust]
        toppings_price = sum(
            amount * self.TOPPING_PRICE for amount in self.toppings.values()
        )
        total_price = base_price + crust_price + toppings_price
        return round(total_price, 2)

    def __str__(self):
        """String representation of the pizza."""
        toppings_str = (
            ", ".join(
                f"{topping} (x{amount})" for topping, amount in self.toppings.items()
            )
            or "None"
        )
        return (
            f"Pizza size: {self.size}, Crust: {self.crust}, "
            f"Toppings: {toppings_str}, Total Price: ${self.calculate_price()}"
        )


# Example Usage
pizza = Pizza()
print(pizza)

pizza.add_topping("pepperoni", 2)
pizza.add_topping("mushrooms", 1)
pizza.change_size("large")
pizza.change_crust("stuffed")
pizza.remove_topping("pepperoni", 1)
pizza.remove_topping("mushrooms", 1)
print(pizza)
