class Pizza:
    # Base prices for different sizes and crusts
    size_prices = {"small": 8.0, "medium": 10.0, "large": 12.0}

    crust_prices = {"thin": 2.0, "thick": 2.5, "stuffed": 3.5}

    # Price per topping
    topping_price = 1.5

    def __init__(self, size="medium", crust="thin", toppings=None):
        if toppings is None:
            toppings = []
        self.size = size
        self.crust = crust
        self.toppings = toppings

    def calculate_price(self):
        # Base price from size
        price = self.size_prices.get(self.size.lower(), 10.0)

        # Add price for crust
        price += self.crust_prices.get(self.crust.lower(), 2.0)

        # Add price for each topping
        price += len(self.toppings) * self.topping_price

        return price

    def __str__(self):
        toppings_list = ", ".join(self.toppings) if self.toppings else "no toppings"
        return (
            f"Pizza Size: {self.size.capitalize()}, Crust: {self.crust.capitalize()}, "
            f"Toppings: {toppings_list}, Total Price: ${self.calculate_price():.2f}"
        )


# Example usage:
pizza = Pizza(
    size="large", crust="stuffed", toppings=["pepperoni", "mushrooms", "olives"]
)
print(pizza)
