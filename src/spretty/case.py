from rich.console import RenderableType
from rich.text import Text


class Case:
    class ID:
        def __init__(self, target, case, test):
            self.target = target
            self.case = case
            self.test = test

    def __init__(self, id: ID, status: str, duration: str):
        self.id = id
        self.status = status
        self.duration = duration

    def started_text(self) -> RenderableType:
        name = self.id.test
        if name.endswith("__pass"):
            name = name[:-6]

        text = Text()
        text.append(name, style="green")
        text.append(" ...", style="green")
        return text

    def passed_text(self) -> RenderableType:
        name = self.id.test
        if name.endswith("__pass"):
            name = name[:-6]

        text = Text()
        text.append(name, style="blue")
        text.append("  ", style="blue")
        return text

    def failed_text(self) -> RenderableType:
        name = self.id.test
        if name.endswith("__pass"):
            name = name[:-6]

        text = Text()
        text.append(name, style="red")
        text.append(" ✗ ", style="red")
        return text
