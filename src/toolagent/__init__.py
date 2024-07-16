"""Python Package named ToolAgent (A Highly-Modularized Tool Learning Framework for LLM Based Agent)"""

from toolagent._version import __version__
from toolagent.utils._log import setup_logging as _setup_logging

logger = _setup_logging()

__all__ = [
    "__version__",
]


logger.info("ToolAgent (ta) initialization is completed.")
