import textwrap
from os.path import exists

from rich.console import Group
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

CODE_WIDTH = 90


def wrap(text, width=CODE_WIDTH):
    return "\n".join(textwrap.wrap(text, width, subsequent_indent="\x20" * 9))


class Error:
    def __init__(self, file, line, column, kind, message) -> None:
        self.file: str = file
        self.line: str = line
        self.column: str = column
        self.kind: str = kind
        self.message: str = message

    def panel(self) -> Panel:
        kind = Text(wrap(f"Kind:    {self.kind}"))
        path = Text(wrap(f"Path:    {self.file}"))
        line = Text(wrap(f"Line:    {self.line}"))
        message = Text(wrap(f"Message: {self.message}"))

        items = [
            kind,
            path,
            line,
            message,
        ]

        if exists(self.file):
            with open(self.file) as f:
                lines = f.readlines()
                line = int(self.line)
                context = 5
                start = max(0, line - context)
                end = min(len(lines) + 1, line + context)

                codes = Syntax(
                    "".join(lines),
                    "swift",
                    theme="monokai",
                    line_numbers=True,
                    line_range=(start, end),
                    highlight_lines={line},
                    code_width=CODE_WIDTH,
                    # background_color="default",
                )

                sep = Text("𐫴" * (CODE_WIDTH + 4), style="#333333")
                items += [sep, codes]

        group = Group(*items, fit=True)

        if "error" in self.kind:
            title = "[red]  Error"
        else:
            title = "[magenta]  Warning"

        panel = Panel.fit(
            group,
            title=title,
            title_align="left",
        )

        return panel
