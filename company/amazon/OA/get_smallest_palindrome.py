from collections import defaultdict
from collections import OrderedDict


class Solution:
    def computeEncodedProductName(self, nameString: str) -> str:

        # Create a dictionary to count occurrences of each character
        char_count = defaultdict(int)
        n = len(nameString)
        for c in nameString:
            char_count[c] += 1

        # Sort the dictionary in reverse order
        sorted_char_count = OrderedDict(
            sorted(char_count.items(), key=lambda x: x[0], reverse=True)
        )

        # Initialize the result as a list (string builder equivalent in Python)
        result = []

        # If the length of the string is odd, handle the middle character
        if n % 2 != 0:
            middle_char = nameString[n // 2]
            result.append(middle_char)
            sorted_char_count[middle_char] -= 1
            if sorted_char_count[middle_char] == 0:
                del sorted_char_count[middle_char]

        # Build the result string by appending characters to the front and back
        while sorted_char_count:
            ch, count = sorted_char_count.popitem(last=False)
            for _ in range(count // 2):
                result.insert(0, ch)
                result.append(ch)

        return "".join(result)
