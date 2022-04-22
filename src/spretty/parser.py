import re
from collections import namedtuple

from .case import Case
from .error import Error
from .suite import Suite

suite = namedtuple("suite", ["name", "status", "time"])

SUITE_PAT = re.compile(
    r"""
    ^
    Test\sSuite
    \s+
    '(?P<name>[^']+)'         # suite name
    \s+
    (?P<status>\w+)           # suite status
    \s+at\s+
    (?P<time>.*?)             # timestamp
    \.?
    $
    """,
    re.VERBOSE,
)


CASE_ID_PAT = re.compile(
    r"""
    ^
    -\[
    (?P<target>\w+)           # test target
    \.
    (?P<case>\w+)             # test case
    \s+
    (?P<test>\w+)             # test
    \]
    $
    """,
    re.VERBOSE,
)

CASE_PAT = re.compile(
    r"""
    ^
    Test\sCase
    \s+
    '(?P<id>.*)'
    \s+
    (?P<status>started|(passed|failed)\s\((?P<time>.*)\))
    \.?
    $
    """,
    re.VERBOSE,
)

ERROR_PAT = re.compile(
    r"""
    ^
    (?P<file>.*?)
    :(?P<line>\d+)
    (?::(?P<column>\d+))?
    :\s+(?P<kind>.*?)
    :\s+(?P<message>.*)
    $
    """,
    re.VERBOSE,
)


def parse_suite_line(line: str) -> Suite | None:
    m = SUITE_PAT.match(line.strip())
    if m is not None:
        return Suite(**m.groupdict())


def parse_case_line(line: str) -> Case | None:
    m = CASE_PAT.match(line.strip())
    if m is not None:
        id = m.group("id")
        id = CASE_ID_PAT.match(id)
        assert id is not None
        id = Case.ID(**id.groupdict())

        return Case(
            id=id,
            status=m.group("status"),
            duration=m.group("time"),
        )


def parse_error_line(line: str) -> Error | None:
    m = ERROR_PAT.match(line.strip())
    if m is not None:
        return Error(**m.groupdict())
