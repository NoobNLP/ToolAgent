from typing import Protocol, runtime_checkable
from typing import Any

@runtime_checkable
class EmbedderProtocol(Protocol):
    def call(self) -> Any:
        ...