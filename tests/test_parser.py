import pytest

from spretty import parser


@pytest.fixture
def sample_lines():
    return [line for line in open("tests/data/swift-test.txt")]


@pytest.fixture
def sample_error_lines():
    return [line for line in open("tests/data/swift-test-error.txt")]


def test_suite_pattern(sample_lines):
    for n in (0, 5, 8):
        line = sample_lines[n]
        case = parser.parse_suite_line(line)
        assert case is None

    line = sample_lines[2]
    suite = parser.parse_suite_line(line)
    assert suite is not None
    assert suite.name == "All tests"
    assert suite.status == "started"
    assert suite.time == "2022-04-22 14:00:49.036"


def test_case_pattern(sample_lines):
    for n in (0, 4, 8):
        line = sample_lines[n]
        case = parser.parse_case_line(line)
        assert case is None


def test_error_pattern(sample_error_lines):
    line = sample_error_lines[1]
    error = parser.parse_error_line(line)
    assert error is not None
    assert error.path.endswith("DASwift/RotateImage.swift")
    assert error.line == "4"
    assert error.column == "43"
    assert error.kind == "error"
    assert error.message == "expected ',' separator"
