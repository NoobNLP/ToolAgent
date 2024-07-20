from typing import Protocol, runtime_checkable
from typing import Any

@runtime_checkable
class ToolProtocol(Protocol):
    tool_name: str
    tool_description: str
    tool_hash: str
    def call(self) -> Any:
        ...