"""Python Package named ToolAgent (A Highly-Modularized Tool Learning Framework for LLM Based Agent)"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

from toolagent.utils.config import get_config
from toolagent.utils.logging import get_logger

__all__ = [
    "__version__",
    "config",
    "logger"
]

# Official PEP 396
try:
    __version__ = version("toolagent")
except PackageNotFoundError:
    __version__ = "unknown version"

config = get_config()
logger = get_logger()


logger.info("ToolAgent (TA) initialization is completed.")
