"""Python Package named ToolAgent (A Highly-Modularized Tool Learning Framework for LLM Based Agent)"""

from src.toolagent.utils.logging import setup_logging as _setup_logging
from toolagent._version import __version__

logger = _setup_logging()

__all__ = [
    "__version__",
]


logger.info("ToolAgent (ta) initialization is completed.")
