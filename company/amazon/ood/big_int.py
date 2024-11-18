class BigInt:
    def __init__(self, value):
        # Handle initialization from both string and integer inputs
        if isinstance(value, str):
            if not value.isdigit():
                raise ValueError("String must contain only digits")
            self.digits = [int(digit) for digit in value]
        elif isinstance(value, int):
            self.digits = [int(digit) for digit in str(value)]
        else:
            raise TypeError("BigInt must be initialized with a string or an integer")

    def __str__(self):
        # Convert the list of digits back into a string
        return "".join(map(str, self.digits))

    def __eq__(self, other):
        # Check equality of two BigInt objects
        if isinstance(other, BigInt):
            return self.digits == other.digits
        return False

    def __lt__(self, other):
        # Compare two BigInt objects
        if isinstance(other, BigInt):
            if len(self.digits) != len(other.digits):
                return len(self.digits) < len(other.digits)
            return self.digits < other.digits
        return False

    def __add__(self, other):
        if not isinstance(other, BigInt):
            raise TypeError("Operand must be a BigInt")

        # Ensure both numbers have the same length by padding the shorter one with zeros
        max_len = max(len(self.digits), len(other.digits))
        a = [0] * (max_len - len(self.digits)) + self.digits
        b = [0] * (max_len - len(other.digits)) + other.digits

        carry = 0
        result = []

        # Add digits from right to left
        for i in range(max_len - 1, -1, -1):
            total = a[i] + b[i] + carry
            result.insert(0, total % 10)
            carry = total // 10

        # If there is a carry left over at the end
        if carry:
            result.insert(0, carry)

        return BigInt("".join(map(str, result)))

    def __sub__(self, other):
        # Handle basic subtraction assuming self is greater than or equal to other
        if not isinstance(other, BigInt):
            raise TypeError("Operand must be a BigInt")

        if self < other:
            raise ValueError(
                "Subtraction result would be negative, which is not supported"
            )

        max_len = max(len(self.digits), len(other.digits))
        a = [0] * (max_len - len(self.digits)) + self.digits
        b = [0] * (max_len - len(other.digits)) + other.digits

        result = []
        borrow = 0

        for i in range(max_len - 1, -1, -1):
            diff = a[i] - b[i] - borrow
            if diff < 0:
                diff += 10
                borrow = 1
            else:
                borrow = 0
            result.insert(0, diff)

        # Remove leading zeros
        while len(result) > 1 and result[0] == 0:
            result.pop(0)

        return BigInt("".join(map(str, result)))

    def __mul__(self, other):
        if not isinstance(other, BigInt):
            raise TypeError("Operand must be a BigInt")

        a_len = len(self.digits)
        b_len = len(other.digits)
        result = [0] * (a_len + b_len)

        # Multiply each digit
        for i in range(a_len - 1, -1, -1):
            carry = 0
            for j in range(b_len - 1, -1, -1):
                total = result[i + j + 1] + self.digits[i] * other.digits[j] + carry
                result[i + j + 1] = total % 10
                carry = total // 10
            result[i + j] += carry

        # Convert the result list back to BigInt, removing leading zeros
        while len(result) > 1 and result[0] == 0:
            result.pop(0)

        return BigInt("".join(map(str, result)))


# Example usage:
num1 = BigInt("123456789123456789")
num2 = BigInt("987654321987654321")

print("Addition:", num1 + num2)  # Output: BigInt with result of the addition
print("Subtraction:", num2 - num1)  # Output: BigInt with result of the subtraction
print(
    "Multiplication:", num1 * num2
)  # Output: BigInt with result of the multiplication
