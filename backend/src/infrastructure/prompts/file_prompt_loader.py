from __future__ import annotations

from pathlib import Path


class FilePromptLoader:
    def __init__(self, root: Path) -> None:
        self._root = root

    def load(self, name: str) -> str:
        prompt_path = (self._root / f"{name}.md").resolve()
        root = self._root.resolve()
        if not str(prompt_path).startswith(str(root)):
            raise ValueError(f"prompt path is outside root: {name}")
        return prompt_path.read_text(encoding="utf-8")
