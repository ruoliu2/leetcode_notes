import unittest
from io import StringIO
from contextlib import redirect_stdout
from atlas import normalize, check_availability


class TestNormalize(unittest.TestCase):
    """Test cases for the normalize function"""
    
    def test_combination(self):
        """Test combinations of normalization rules"""
        assert normalize("The Llama Industries, Inc.") == "llama industries"
        assert normalize("An Llama & Industries, LLC") == "llama industries"
        assert normalize("The Llama and Industries and Co, Inc.") == "llama industries co"
        # Only allowed suffixes are stripped; 'Corp' (no dot) stays
        assert normalize("A & B Corp") == "b corp"

    def test_empty_and_edge_cases(self):
        """Edge cases that result in empty strings"""
        assert normalize("") == ""
        assert normalize("   ") == ""
        assert normalize("The") == ""          # leading article only -> empty
        assert normalize("Inc.") == ""         # allowed suffix-only -> empty
        assert normalize("The Inc.") == ""     # article + allowed suffix-only -> empty
        # 'Corp.' (with dot) is allowed -> can vanish after removing leading article
        assert normalize("A Corp.") == ""

    def test_punctuation_replacement(self):
        """& and , become spaces; multiple spaces collapse"""
        # also validates that non-allowed suffix 'Corp' (no dot) remains
        assert normalize("A,&,B,,Corp") == "b corp"

    def test_suffixes(self):
        """Only allowed suffix tokens are stripped; others remain"""
        # Allowed and should be stripped:
        assert normalize("Llama Inc.") == "llama"
        assert normalize("Llama Corp.") == "llama"
        assert normalize("Llama LLC") == "llama"
        assert normalize("Llama LLC.") == "llama"
        assert normalize("Llama L.L.C.") == "llama"

        # Not allowed → should NOT be stripped:
        assert normalize("Llama Inc") == "llama inc"     # missing dot
        assert normalize("Llama Corp") == "llama corp"   # missing dot

        # Wrong dot pattern should remain:
        assert normalize("Llama L.LC.") == "llama l.lc."   # not exact L.L.C.
        assert normalize("Llama L.L.C") == "llama l.l.c"   # missing final dot


    def test_basic_normalization(self):
        """Test basic normalization with common company name formats"""
        self.assertEqual(normalize("Llama Industries"), "llama industries")
        self.assertEqual(normalize("Llama Industries, Inc."), "llama industries")
        self.assertEqual(normalize("Llama Industries Inc."), "llama industries")
        self.assertEqual(normalize("Llama Industries LLC"), "llama industries")
        self.assertEqual(normalize("Llama Industries, L.L.C."), "llama industries")

    def test_case_insensitive(self):
        """Test that normalization is case-insensitive"""
        self.assertEqual(normalize("LLAMA INDUSTRIES"), "llama industries")
        self.assertEqual(normalize("LlAmA InDuStRiEs"), "llama industries")
        self.assertEqual(normalize("llama industries"), "llama industries")

    def test_leading_articles(self):
        """Test removal of leading articles (the, an, a)"""
        self.assertEqual(normalize("The Llama Industries"), "llama industries")
        self.assertEqual(normalize("An Llama Industries"), "llama industries")
        self.assertEqual(normalize("A Llama Industries"), "llama industries")
        self.assertEqual(normalize("The Llama Industries, Inc."), "llama industries")

    def test_article_not_leading(self):
        """Test that articles in the middle are not removed"""
        self.assertEqual(normalize("Llama The Industries"), "llama the industries")


    def test_and_word_removal(self):
        """Test removal of 'and' word except when it's the first word"""
        self.assertEqual(normalize("Llama and Industries"), "llama industries")
        self.assertEqual(normalize("Llama and Industries and Co"), "llama industries co")
        self.assertEqual(normalize("and Llama Industries"), "and llama industries")  # First word kept
        self.assertEqual(normalize("And Llama Industries"), "and llama industries")  # First word kept


    def test_whitespace_collapse(self):
        """Test collapsing of multiple spaces"""
        self.assertEqual(normalize("Llama   Industries"), "llama industries")
        self.assertEqual(normalize("Llama    Industries    Inc."), "llama industries")

    def test_strip_dots_in_suffix(self):
        """Test that dots are stripped when checking suffixes"""
        self.assertEqual(normalize("Llama L.L.C."), "llama")
        self.assertEqual(normalize("Llama Inc."), "llama")


class TestCheckAvailability(unittest.TestCase):
    """Test cases for the check_availability function"""

    def test_single_request(self):
        """Test a single request should be available"""
        lines = ["acct_12345 | Llama Industries"]
        f = StringIO()
        with redirect_stdout(f):
            check_availability(lines)
        output = f.getvalue().strip()
        self.assertEqual(output, "acct_12345 | Name Available")

    def test_duplicate_request(self):
        """Test duplicate requests - second should be not available"""
        lines = [
            "acct_12345 | Llama Industries",
            "acct_54321 | Llama Industries"
        ]
        f = StringIO()
        with redirect_stdout(f):
            check_availability(lines)
        output = f.getvalue().strip().split("\n")
        self.assertEqual(output[0], "acct_12345 | Name Available")
        self.assertEqual(output[1], "acct_54321 | Name Not Available")

    def test_normalized_duplicates(self):
        """Test that different formats normalize to same name"""
        lines = [
            "acct_12345 | Llama Industries, Inc.",
            "acct_54321 | The Llama Industries, LLC",
            "acct_99999 | llama industries"
        ]
        f = StringIO()
        with redirect_stdout(f):
            check_availability(lines)
        output = f.getvalue().strip().split("\n")
        self.assertEqual(output[0], "acct_12345 | Name Available")
        self.assertEqual(output[1], "acct_54321 | Name Not Available")
        self.assertEqual(output[2], "acct_99999 | Name Not Available")

    def test_case_insensitive_duplicates(self):
        """Test case-insensitive duplicate detection"""
        lines = [
            "acct_12345 | LLAMA INDUSTRIES",
            "acct_54321 | llama industries"
        ]
        f = StringIO()
        with redirect_stdout(f):
            check_availability(lines)
        output = f.getvalue().strip().split("\n")
        self.assertEqual(output[0], "acct_12345 | Name Available")
        self.assertEqual(output[1], "acct_54321 | Name Not Available")

    def test_article_normalization(self):
        """Test that names with articles normalize correctly"""
        lines = [
            "acct_12345 | The Llama Industries",
            "acct_54321 | Llama Industries"
        ]
        f = StringIO()
        with redirect_stdout(f):
            check_availability(lines)
        output = f.getvalue().strip().split("\n")
        self.assertEqual(output[0], "acct_12345 | Name Available")
        self.assertEqual(output[1], "acct_54321 | Name Not Available")

    def test_and_word_normalization(self):
        """Test that 'and' removal works correctly in availability"""
        lines = [
            "acct_12345 | Llama and Industries",
            "acct_54321 | Llama Industries"
        ]
        f = StringIO()
        with redirect_stdout(f):
            check_availability(lines)
        output = f.getvalue().strip().split("\n")
        self.assertEqual(output[0], "acct_12345 | Name Available")
        self.assertEqual(output[1], "acct_54321 | Name Not Available")

    def test_punctuation_normalization(self):
        """Test that punctuation normalization works"""
        lines = [
            "acct_12345 | Llama & Industries",
            "acct_54321 | Llama, Industries"
        ]
        f = StringIO()
        with redirect_stdout(f):
            check_availability(lines)
        output = f.getvalue().strip().split("\n")
        self.assertEqual(output[0], "acct_12345 | Name Available")
        self.assertEqual(output[1], "acct_54321 | Name Not Available")

    def test_empty_name(self):
        """Empty names after normalization are not available"""
        lines = [
            "acct_12345 | The Inc.",
            "acct_54321 | ",
            "acct_99999 |    "
        ]
        f = StringIO()
        with redirect_stdout(f):
            check_availability(lines)
        output = f.getvalue().strip().split("\n")
        assert output[0] == "acct_12345 | Name Not Available"
        assert output[1] == "acct_54321 | Name Not Available"
        assert output[2] == "acct_99999 | Name Not Available"
        
    def test_malformed_input(self):
        """Test malformed input without pipe separator"""
        lines = [
            "acct_12345 | Valid Company Name",
            "acct_54321 no pipe here",
            "just a line"
        ]
        f = StringIO()
        with redirect_stdout(f):
            check_availability(lines)
        output = f.getvalue().strip().split("\n")
        self.assertEqual(output[0], "acct_12345 | Name Available")
        self.assertEqual(output[1], "acct_54321 no pipe here | Name Not Available")
        self.assertEqual(output[2], "just a line | Name Not Available")

    def test_multiple_unique_names(self):
        """Test multiple unique company names"""
        lines = [
            "acct_12345 | Llama Industries",
            "acct_54321 | Alpaca Corp",
            "acct_99999 | Vicuna LLC"
        ]
        f = StringIO()
        with redirect_stdout(f):
            check_availability(lines)
        output = f.getvalue().strip().split("\n")
        self.assertEqual(output[0], "acct_12345 | Name Available")
        self.assertEqual(output[1], "acct_54321 | Name Available")
        self.assertEqual(output[2], "acct_99999 | Name Available")

    def test_complex_example(self):
        """Test complex real-world example from the docstring"""
        lines = [
            "acct_12345 | Llama Industries, Inc.",
            "acct_54321 | The Llama Industries, LLC",
            "acct_99999 | Llama & Industries"
        ]
        f = StringIO()
        with redirect_stdout(f):
            check_availability(lines)
        output = f.getvalue().strip().split("\n")
        self.assertEqual(output[0], "acct_12345 | Name Available")
        self.assertEqual(output[1], "acct_54321 | Name Not Available")
        self.assertEqual(output[2], "acct_99999 | Name Not Available")

    def test_empty_lines(self):
        """Test that empty lines are skipped"""
        lines = [
            "acct_12345 | Llama Industries",
            "",
            "   ",
            "acct_54321 | Alpaca Corp"
        ]
        f = StringIO()
        with redirect_stdout(f):
            check_availability(lines)
        output = f.getvalue().strip().split("\n")
        self.assertEqual(output[0], "acct_12345 | Name Available")
        self.assertEqual(output[1], "acct_54321 | Name Available")

    def test_pipe_in_name(self):
        """Test that only first pipe is used for splitting"""
        lines = [
            "acct_12345 | Company | Name",
            "acct_54321 | Company"
        ]
        f = StringIO()
        with redirect_stdout(f):
            check_availability(lines)
        output = f.getvalue().strip().split("\n")
        # First one normalizes "Company | Name" (pipe treated as part of name, then normalized)
        # Actually, looking at the code, the pipe stays in the name string, but when normalized,
        # it would become "company | name" -> after space collapse "company | name"
        # Second should be available since "Company" normalizes to "company" which is different
        self.assertEqual(output[0], "acct_12345 | Name Available")
        self.assertEqual(output[1], "acct_54321 | Name Available")


if __name__ == "__main__":
    unittest.main()

