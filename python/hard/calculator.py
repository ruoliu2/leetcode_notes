class Solution:
    def calculate(self, s: str) -> int:
        res = cur = num = 0
        op = '+'
        st = []
        s = s.replace(")", "+)")
        for c in f"{s}+":
            if c.isdigit():
                num = num * 10 + int(c)
            elif c in "+-*/":
                if op == "+":
                    cur += num
                if op == "-":
                    cur -= num
                if op == "*":
                    cur *= num
                if op == "/":
                    cur = int(cur / num)
                if c in "+-":
                    res += cur
                    cur = 0
                op = c
                num = 0
            elif c == "(":
                st.append((res, cur, op))
                res, cur, op = 0, 0, '+'
            elif c == ")":
                num = res
                res, cur, op = st.pop()
        return res
