from rich.console import RenderableType
from rich.text import Text


class Suite:
    def __init__(self, name, status, time):
        self.name = name
        self.status = status
        self.time = time

    def text(self) -> RenderableType:
        text = Text()
        text.append(self.name, style="bold magenta")
        return text
