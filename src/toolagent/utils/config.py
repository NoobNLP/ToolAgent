"""Config of the ToolAgent package which contains all kinds of settings and basic information about the job.
"""

import datetime

import pydantic

class ToolAgentConfig(pydantic.BaseModel):
    """
    """
    job_time: str
    type_check: bool = True


def get_config():
    return ToolAgentConfig(
        job_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        type_check = True
    )