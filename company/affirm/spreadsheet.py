"""
SpreadSheet Filter (Affirm)

Read file, parse rows, filter by column conditions.

Example file (a.txt):
  color date number
  green 2001/02/23 8
  purple 2006/05/11 1
  white 2019/02/17 200

Usage:
  sheet = SpreadSheet("a.txt")
  sheet.filter(['color', '=', 'green'])  # [['green', '2001/02/23', '8']]
"""


class SpreadSheet:
    def __init__(self, filepath: str):
        self.headers = []
        self.rows = []
        self._parse(filepath)

    def _parse(self, filepath: str):
        with open(filepath) as f:
            lines = [line.strip() for line in f if line.strip()]

        self.headers = lines[0].split()
        self.rows = [line.split() for line in lines[1:]]

    def _matches(self, row: list[str], condition: list) -> bool:
        """Check if row matches a single condition."""
        col_name, op, value = condition
        col_idx = self.headers.index(col_name)
        cell = row[col_idx]
        ops = {
            "=": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
            ">": lambda a, b: float(a) > float(b),
            "<": lambda a, b: float(a) < float(b),
            ">=": lambda a, b: float(a) >= float(b),
            "<=": lambda a, b: float(a) <= float(b),
        }
        return ops[op](cell, value)

    def filter(self, condition: list) -> list[list[str]]:
        """Filter by single condition: [column_name, operator, value]"""
        return [row for row in self.rows if self._matches(row, condition)]

    def filter_multi(self, conditions: list[list]) -> list[list[str]]:
        """Multiple conditions with AND logic."""
        return [row for row in self.rows if all(self._matches(row, c) for c in conditions)]


# For testing without actual file
class SpreadSheetFromData(SpreadSheet):
    def __init__(self, data: str):
        self.headers = []
        self.rows = []
        lines = [line.strip() for line in data.strip().split("\n") if line.strip()]
        self.headers = lines[0].split()
        self.rows = [line.split() for line in lines[1:]]


if __name__ == "__main__":
    data = """
    color date number
    green 2001/02/23 8
    purple 2006/05/11 1
    white 2019/02/17 200
    green 2020/01/01 50
    """

    sheet = SpreadSheetFromData(data)

    print("Filter color = green:")
    print(sheet.filter(["color", "=", "green"]))
    # [['green', '2001/02/23', '8'], ['green', '2020/01/01', '50']]

    print("\nFilter number > 10:")
    print(sheet.filter(["number", ">", "10"]))
    # [['white', '2019/02/17', '200'], ['green', '2020/01/01', '50']]

    print("\nFilter color = green AND number > 10:")
    print(sheet.filter_multi([["color", "=", "green"], ["number", ">", "10"]]))
    # [['green', '2020/01/01', '50']]
