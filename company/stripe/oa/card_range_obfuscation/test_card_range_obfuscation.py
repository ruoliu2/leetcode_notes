import pytest
from card_range_obfuscation import (
    obfuscate_card_ranges,
    parse_input_lines,
    format_output,
    OFFSET_MAX,
)

def make(card):
    # helper to slice start,end,brand for readability in assertions
    return {"start": card[0], "end": card[1], "brand": card[2]}

def test_example_input_is_formatted_and_filled_to_full_range():
    # Given example (two contiguous intervals); per spec we ensure FULL coverage by extending
    bin6 = "777777"
    intervals = [
        (1_000_000_000, 3_999_999_999, "VISA"),
        (4_000_000_000, 5_999_999_999, "MASTERCARD"),
    ]
    out = obfuscate_card_ranges(bin6, intervals)

    # Expect three output segments covering 0..9_999_999_999:
    # 1) Extend first backward to 0 (brand VISA)
    # 2) As provided seam (VISA to MASTERCARD remains)
    # 3) Extend last forward to MAX (brand MASTERCARD)
    # But because we extend by editing endpoints, we actually produce just TWO intervals:
    #   - First: VISA from 0 .. 3_999_999_999 (extended backward)
    #   - Second: MASTERCARD from 4_000_000_000 .. 9_999_999_999 (extended forward)
    # (No gap existed in the middle, so no extra segment is needed.)
    assert len(out) == 2

    first, second = map(make, out)
    assert first["start"] == "7777770000000000"
    assert first["end"]   == "7777773999999999"
    assert first["brand"] == "VISA"

    assert second["start"] == "7777774000000000"
    assert second["end"]   == "7777779999999999"
    assert second["brand"] == "MASTERCARD"

def test_fill_middle_gap_by_extending_previous():
    bin6 = "424242"
    intervals = [
        (100, 199, "VISA"),
        (300, 350, "MC"),
    ]
    out = obfuscate_card_ranges(bin6, intervals)
    # After normalization:
    # - Extend first backward to 0
    # - Fill middle gap (200..299) by extending VISA forward to 299
    # - MC keeps 300..350 and is extended to MAX
    # => Two intervals total: (VISA 0..299) and (MC 300..MAX)
    assert len(out) == 2

    first, second = out

    # First interval (VISA) covers 0..299
    assert first[0] == "4242420000000000"
    assert first[1].endswith(f"{299:010d}")
    assert first[2] == "VISA"

    # Second interval (MC) covers 300..MAX
    assert second[0].endswith(f"{300:010d}")
    from card_range_obfuscation import OFFSET_MAX
    assert second[1].endswith(f"{OFFSET_MAX:010d}")
    assert second[2] == "MC"


def test_overlap_different_brands_keeps_earlier_and_shifts_later():
    bin6 = "555555"
    intervals = [
        (1000, 2500, "VISA"),
        (2000, 3000, "AMEX"),  # overlaps; must shift to start at 2501
    ]
    out = obfuscate_card_ranges(bin6, intervals)
    # After full coverage:
    # - First extends back to 0, remains VISA 0..2500
    # - Second shifts to 2501..3000, then final extension to MAX with AMEX
    # => Two intervals: VISA 0..2500, AMEX 2501..MAX
    assert len(out) == 2
    first, second = out
    assert first[0] == "5555550000000000"
    assert first[1].endswith(f"{2500:010d}")
    assert first[2] == "VISA"

    assert second[0].endswith(f"{2501:010d}")
    assert second[1].endswith(f"{OFFSET_MAX:010d}")
    assert second[2] == "AMEX"

def test_adjacent_same_brand_merges():
    bin6 = "123456"
    intervals = [
        (0, 100, "VISA"),
        (101, 200, "VISA"),  # merges with previous
    ]
    out = obfuscate_card_ranges(bin6, intervals)
    # Merged first two → 0..200 VISA, then extend to MAX with VISA (still one brand)
    assert len(out) == 1
    only = out[0]
    assert only[0] == "1234560000000000"
    assert only[1].endswith(f"{OFFSET_MAX:010d}")
    assert only[2] == "VISA"

def test_parse_and_format_helpers_round_trip():
    lines = [
        "777777",
        "2",
        "1000000000,3999999999,VISA",
        "4000000000,5999999999,MASTERCARD",
    ]
    bin6, ivs = parse_input_lines(lines)
    assert bin6 == "777777"
    assert ivs == [
        (1_000_000_000, 3_999_999_999, "VISA"),
        (4_000_000_000, 5_999_999_999, "MASTERCARD"),
    ]
    out = obfuscate_card_ranges(bin6, ivs)
    # Format: "start,end,brand"
    lines = format_output(out)
    # First must start at BIN..0000000000 per full-coverage rule
    assert lines[0].startswith("7777770000000000,")
    assert lines[0].endswith(",VISA")
    assert lines[1].endswith(",MASTERCARD")

def test_no_intervals_is_error():
    with pytest.raises(ValueError):
        obfuscate_card_ranges("777777", [])
