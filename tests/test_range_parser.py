import pytest

from pdf_toolbox.core.range_parser import RangeParseError, parse_page_range


def test_parse_simple_range():
    assert parse_page_range("1-3") == [0, 1, 2]


def test_parse_mixed_ranges():
    assert parse_page_range("1-3,8,10-12") == [0, 1, 2, 7, 9, 10, 11]


def test_parse_duplicate_pages():
    assert parse_page_range("1,1,2") == [0, 1]


def test_parse_invalid():
    with pytest.raises(RangeParseError):
        parse_page_range("a-b")


def test_parse_out_of_bounds():
    with pytest.raises(RangeParseError):
        parse_page_range("1-3", max_pages=2)


