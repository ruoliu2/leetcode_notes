'''
###### Atlas Company Name Check

Stripe Atlas enables founders to remotely incorporate a US-based company from anywhere in the world. Founders provide us the name they want for their company, and Stripe does some internal validation to make sure that the name isn't being used by another company.
However, names don't have be exactly identical to be considered the same. The government also disallows names that are too similar and could be confused for other companies.
Your task

1. Complete the function `check_availability, which takes in a list of account IDs and its corresponding name request.
2. For each requested name, make a determination of Name Available or Name Not Available, based on the name's availability.
3. If the name is currently available, we will print that it is available and mark the name as no longer available.
4. If the name is not available, print that it is unavailable.

Beyond identical characters, there are several additional rules used to determine if two company names are the same:

- Capitalization is ignored, eg: "Llama, Inc." is the same as "LLAMA, Inc."
- Ampersands ("&"), commas (".") are treated as spaces (" ").
- Multiple spaces in a row are treated as as single space.
- Company name suffixes are ignored, eg: "Llama, Inc." is the same as "Llama, LLC."
- You can assume that all company names will have a suffix, and that all suffixes will be one of ["Inc.", "Corp.", "LLC", "L.L.C.", "LLC."] (case-insensitive)

- Leading The. An, and A are ignored, (eg: "Llama, Inc." is the same as "The Llama, Inc.") And is ignored, unless it is at the beginning of the company name, eg: "Llama Friend, Inc." is the same as "Llama And Friend, Inc." but different from "And Llama Friend, Inc."
- After the transformations above, if the name is empty or only contains spaces, it should be considered Not Available

Input

Each line of input will represent a name availability check with an account_id (eg:acct_xyz) and a proposed name. The fields will be split with a | (pipe)
character.

Output

Print one line for each merchant request. The line should include the merchant id, followed by a pipe (1), followed by either a string Name Available or Name Not Available

Examples

Example 1 - Single Entry
Input
acct_12345 | Llama Industries, Inc.
Output
acct_12345 | Name Available
Explanation
We received one name request for a single merchant. The name was not taken so we reported it as available.
'''

import sys
import re
from typing import Iterable, Set

# Precompiled helpers
SPACEIFY = re.compile(r"[&,]")                      # &, , -> space
MULTISPACE = re.compile(r"\s+")
# handle "the", "an", "a" at start, whether followed by space or end-of-string
LEADING_ARTICLE = re.compile(r"^(?:the|an|a)(?=\s+|$)\s*", re.I)
# allow: inc / inc. / corp / corp. / llc / llc. / l.l.c.
TRAILING_SUFFIX = re.compile(r"(?:^|\s)(?:inc\.|corp\.|llc\.?|l\.l\.c\.)\s*$", re.I)

def normalize(name: str) -> str:
    s = name.strip().lower()
    if not s:
        return ""

    s = SPACEIFY.sub(" ", s)           # & , -> space
    s = MULTISPACE.sub(" ", s).strip() # collapse spaces

    # strip trailing company suffix (flexible set above)
    s = TRAILING_SUFFIX.sub("", s).strip()
    if not s:
        return ""

    # drop leading article even if it is the only token
    s = LEADING_ARTICLE.sub("", s).strip()
    if not s:
        return ""

    tokens = s.split()
    first, rest = tokens[0], [t for t in tokens[1:] if t != "and"]
    return " ".join([first] + rest).strip()

def check_availability(lines: Iterable[str]) -> None:
    """
    Reads lines like: acct_123 | Llama Industries, Inc.
    Prints: acct_123 | Name Available / Name Not Available
    Marks a normalized name as taken once approved.
    """
    taken: Set[str] = set()

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        acct, sep, proposed = line.partition("|")
        if not sep:
            # Malformed; cannot parse => Not Available
            print(f"{line} | Name Not Available")
            continue

        acct_id = acct.strip()
        key = normalize(proposed.strip())
        if not key or key in taken:
            print(f"{acct_id} | Name Not Available")
        else:
            print(f"{acct_id} | Name Available")
            taken.add(key)

if __name__ == "__main__":
    check_availability(sys.stdin)
