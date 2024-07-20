from toolagent.utils.random import calculate_tool_hash

class LocalTool:
    """Tool

    Attributes:
        tool_name (str):
        tool_description (str):
        tool_set (str):
        tool_id (str): Unique identifier for the tool.
    
    """
    def __init__(self):
        self.tool_name = None
        self.tool_description = None
        self.tool_set = None #来源于哪个工具集，如API-Bank

        self.tool_id = calculate_tool_hash(...) # import hashlib, 用工具名称、描述、参数、返回值等所有信息生成hash

    def __call__(self):
        result = eval()
        return result