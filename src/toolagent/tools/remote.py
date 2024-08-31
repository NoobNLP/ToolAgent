import importlib
from typing import Dict, List, Any, Callable
import requests
from toolagent.utils.random import calculate_tool_hash
from toolagent.types.proto import ToolProtocol

class RemoteTool(ToolProtocol):
    """This class defines the base class for tools that can be executed remotely.

    Attributes:
        tool_name (str): the name of the tool, which must be passed in
        tool_description (str): the description of the tool
        tool_set (str): the set the tool belongs to
        input_parameters (Dict[str, Any]): the detailed information of the input parameters
        output_parameters (Dict[str, Any]): the detailed information of the output parameters
        required (List[str]): the list of the names of the required input parameters
        executable (bool): whether the tool is executable
        url (str): the url of the remote tool
        

    Example:
        pass
    """

    def __init__(self, tool_name: str, tool_description: str = None, tool_set: str = None, input_parameters: Dict[str, Any] = None, output_parameters: Dict[str, Any] = None, required_parameters: List[str] = None, executable: bool = True, url: str = None):
        self.tool_name = tool_name
        self.tool_description = tool_description
        self.tool_set = tool_set
        self.input_parameters = input_parameters
        self.output_parameters = output_parameters
        self.required = required_parameters
        self.tool_id = calculate_tool_hash(self.tool_name, self.tool_description, self.tool_set, self.input_parameters, self.output_parameters) 
        self.executable = executable
        self.url = url 
        
        
        if self.executable:
            assert self.url 

        

        

    def __call__(self, param_dict: Dict[str, Any], modify_url: Callable[[str, Dict[str, Any]], str], **kwargs: Any):
        url = modify_url(self.url, param_dict)
        response = requests.get(url, kwargs)
        try:
            observation = response.json()
            return {"response": observation}
        except Exception as e:
            observation = response.text
            return {"error": str(e), "response": observation}
            
            

if __name__ == "__main__":
    pass
