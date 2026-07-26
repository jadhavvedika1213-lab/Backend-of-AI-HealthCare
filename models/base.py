from datetime import datetime, timezone
from typing import Any


class Document:
    def __init__(self, **values: Any) -> None:
        for name, value in self.defaults().items():
            setattr(self, name, value() if callable(value) else value)
        for name, value in values.items():
            setattr(self, name, value)

    @classmethod
    def defaults(cls) -> dict[str, Any]:
        return {}

    @classmethod
    def from_document(cls, document: dict[str, Any] | None):
        if document is None:
            return None
        return cls(**{key: value for key, value in document.items() if key != "_id"})

    def to_document(self) -> dict[str, Any]:
        return dict(self.__dict__)


def now() -> datetime:
    return datetime.now(timezone.utc)
