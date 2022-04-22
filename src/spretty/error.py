from os.path import exists

from rich.console import Group
from rich.panel import Panel
from rich.syntax import Syntax


class Error:
    def __init__(self, file, line, column, kind, message) -> None:
        self.file: str = file
        self.line: str = line
        self.column: str = column
        self.kind: str = kind
        self.message: str = message

    def panel(self) -> Panel:
        items = [
            f"Kind:    {self.kind}",
            f"Path:    {self.file}",
            f"Line:    {self.line}",
            f"Message: {self.message}",
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
                    code_width=90,
                    # background_color="default",
                )

                items += ["\n", codes]

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
