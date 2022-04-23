import fileinput
from typing import List

from rich.console import Console, RenderableType
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree

from spretty import parser
from spretty.case import Case


def badge(content: str) -> RenderableType:
    text = Text()
    text.append(content)

    panel = Panel.fit(text, style="yellow")
    return panel


def main():
    root: Tree | None = None

    _stack: List[Tree] = []  # suite node stack

    _csn: Tree | None = None  # current suite node

    _cc: Case | None = None  # current case
    _ccn: Tree | None = None  # current case node

    console = Console()
    status = console.status("Buiding tests ...", spinner="aesthetic")
    status.start()

    with fileinput.input() as stdin:
        for line in stdin:
            line = str(line).strip()

            if (suite := parser.parse_suite_line(line)) is not None:
                if suite.status == "started":
                    status.stop()

                    root = Tree(suite.text(), guide_style="green")
                    _stack.append(root)

                    break
                else:
                    raise RuntimeError()

            elif (case := parser.parse_case_line(line)) is not None:
                raise RuntimeError()

            elif (error := parser.parse_error_line(line)) is not None:
                status.stop()
                console.print(error.panel())

            else:
                pass

        print()

        with Live() as live:
            for line in stdin:
                line = str(line).strip()

                if len(_stack) == 0:
                    break

                _csn = _stack[-1]

                if suite := parser.parse_suite_line(line):
                    if suite.status == "started":
                        _csn = _stack[-1]
                        _csn = _csn.add(suite.text())

                        _stack.append(_csn)
                    elif suite.status == "passed":
                        _stack.pop()
                    else:  # failure
                        pass

                elif case := parser.parse_case_line(line):
                    if case.status.startswith("started"):
                        name = case.id.test
                        if name.endswith("__pass"):
                            name = name[:-6]

                        _cc = case
                        _ccn = _csn.add(case.started_text())
                    elif case.status.startswith("passed"):
                        _csn.children[-1] = Tree(case.passed_text())
                    else:
                        pass

                elif error := parser.parse_error_line(line):
                    assert _cc is not None
                    _ccn = Tree(_cc.failed_text())
                    _csn.children[-1] = _ccn

                    assert _ccn is not None
                    _ccn.add(error.panel())
                else:
                    pass

                assert root is not None
                live.update(root)

        print()
        console.print("[yellow] DONE!")


if __name__ == "__main__":
    main()
