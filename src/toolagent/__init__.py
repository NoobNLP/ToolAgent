"""Python Package named ToolAgent (A Highly-Modularized Tool Learning Framework for LLM Based Agent)"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

from toolagent.utils.logging import get_logger

logger = get_logger()

# Official PEP 396
try:
    __version__ = version("toolagent")
except PackageNotFoundError:
    __version__ = "unknown version"

__all__ = [
    "__version__",
]


logger.debug("ToolAgent (ta) initialization is completed.")
