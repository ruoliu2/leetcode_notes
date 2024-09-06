def get_smallest_palindrome(s: str) -> str:
    freq = [0] * 26
    question_marks = 0

    for char in s:
        if char == "?":
            question_marks += 1
        else:
            freq[ord(char) - ord("a")] += 1

    odd = 0
    for i in range(len(freq) - 1, 0, -1):
        if question_marks == 0:
            break
        if freq[i] == 0:
            continue

        if len(s) % 2 != 0:  # if string length is odd
            if freq[i] % 2 != 0:
                odd += 1
                if odd == 1:
                    continue
                else:
                    freq[i] += 1
                    question_marks -= 1
        else:
            if freq[i] % 2 != 0:
                freq[i] += 1
                question_marks -= 1

    if question_marks != 0:
        freq[0] += question_marks

    front = ""
    rear = ""
    mid = ""
    odd = 0

    for i in range(len(freq)):
        ch = chr(i + ord("a"))
        if freq[i] % 2 != 0:
            odd += 1
            if odd > 1:
                return "-1"
            mid += ch * freq[i]
        else:
            front += ch * (freq[i] // 2)
            rear = ch * (freq[i] // 2) + rear

    return front + mid + rear
