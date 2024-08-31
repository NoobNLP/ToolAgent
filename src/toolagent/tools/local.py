from typing import Dict, List, Any, Literal
import importlib
from toolagent.utils.random import calculate_tool_hash
from toolagent.types.proto import ToolProtocol

class LocalTool(ToolProtocol):
    """This class defines the base class for tools which are accessable locally.

    Attributes:
        tool_name (str): the name of the tool, which must be passed in
        tool_description (str): the description of the tool
        tool_set (str): the set the tool belongs to
        input_parameters (Dict[str, Any]): the detailed information of the input parameters
        output_parameters (Dict[str, Any]): the detailed information of the output parameters
        required (List[str]): the list of the names of the required input parameters
        executable (bool): whether the tool is executable, default is True
        executable_type (Literal["class", "function"]): the type of the executable, default is "class"
        path (str): the path to the Python file where the tool is located
        module_name (str): the name of the module to be executed (class or function)
        database (Any): the database information of the tool

    Example:
        pass
    """

    def __init__(self, tool_name: str, tool_description: str = None, tool_set: str = None, input_parameters: Dict[str, Any] = None, output_parameters: Dict[str, Any] = None, required_parameters: List[str] = None, executable: bool = True, executable_type: Literal["class", "function"] = "class", database: Any = None, path: str = None, module_name: str = None):
        self.tool_name = tool_name
        self.tool_description = tool_description
        self.tool_set = tool_set
        self.input_parameters = input_parameters
        self.output_parameters = output_parameters
        self.required = required_parameters
        self.tool_id = calculate_tool_hash(self.tool_name, self.tool_description, self.tool_set, self.input_parameters, self.output_parameters) 
        self.executable = executable
        self.executable_type = executable_type
        self.path = path # the path to be imported, example: toolagent.apibank.lv3_apis.email_reminder
        self.module_name = module_name # name of the module to be executed(class and function), example: TravelStatus
        self.database = database
        
        self.init_func_module = None
        
        if self.executable:
            assert self.path and self.module_name
         

    def import_apply_args(self, *args, **kwargs):
        if self.executable_type == "function":
            module_all = importlib.import_module(f'{self.path}')
            self.init_func_module = getattr(module_all, self.module_name)
            return self.init_func_module
            
            
        elif self.executable_type == "class":
            # exec(f"""from {self.path} import {self.module_name}""")
            module_all = importlib.import_module(f'{self.path}')
            module = getattr(module_all, self.module_name)
            self.init_func_module = module(*args, **kwargs)
            return self.init_func_module
        
        

    def __call__(self, param_dict: Dict):
        if self.executable_type == "function":
            try:
                result = self.init_func_module(**param_dict)
                return {"response": result}
            
            except Exception as e:
                return {"error": str(e)}
            
        elif self.executable_type == "class":
            try:
                result = self.init_func_module.call(**param_dict)
                return {"response": result}
            
            except Exception as e:
                return {"error": str(e)}
            




if __name__ == "__main__":
    parameters = {"tool_name": "example_tool", "tool_description": "This is the tool information","tool_set": "API_bank", "input_parameters": {"a": "asd"}, "output_parameters": {"a": "asd"}, "required_parameters": []}
    example_tool = LocalTool(**parameters)
