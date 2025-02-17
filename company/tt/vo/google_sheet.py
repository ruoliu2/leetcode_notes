class Sheet:
    def __init__(self):
        self.cells = {}  # To store cell values or formulas

    def write(self, cell, value):
        """
        Write a value or formula into a cell.
        """
        self.cells[cell] = value

    def query(self, cell):
        """
        Query the value of a cell. If it contains a formula, evaluate it.
        """
        if cell not in self.cells:
            return "INVALID"  # Return "INVALID" if the cell doesn't exist

        value = self.cells[cell]

        # If the value is an integer, return it directly
        if isinstance(value, int):
            return value

        # If the value is a formula, evaluate it
        if isinstance(value, str) and value.startswith("="):
            try:
                return self._evaluate_formula(value[1:])
            except Exception:
                return "INVALID"  # Invalid formula

        return "INVALID"  # Any other cases are invalid

    def _evaluate_formula(self, formula):
        """
        Evaluate a formula in the format "A1+B2".
        """
        try:
            # Split the formula into two parts
            parts = formula.split("+")
            if len(parts) != 2:
                raise ValueError("Invalid formula")

            # Get the values of the referenced cells
            val1 = self.query(parts[0].strip())
            val2 = self.query(parts[1].strip())

            # Both values must be integers
            if isinstance(val1, int) and isinstance(val2, int):
                return val1 + val2
            else:
                raise ValueError("Invalid cell references")
        except Exception:
            raise ValueError("Invalid formula")


# Example usage
sheet = Sheet()
print(sheet.query("D3"))  # Output: "INVALID"
sheet.write("D3", 5)
print(sheet.query("D3"))  # Output: 5
sheet.write("B1", 3)
sheet.write("C4", "=B1+D3")
print(sheet.query("C4"))  # Output: 8
sheet.write("B1", 10)
print(sheet.query("C4"))  # Output: 15
