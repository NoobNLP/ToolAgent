import re
import json
import os
from typing import Dict, Literal, List
import pkgutil
import importlib
from src.toolagent.tools.local import LocalTool



class APIbankLoader:
    def __init__(self, apis_dir: Literal["apis", "lv3_apis"] = "lv3_apis", database_dir: str = ""):
        """Initialize the APIbankLoader with the directories for APIs and databases.

        Args:
            apis_dir (str): The directory path where the API files are stored.
            database_dir (str): The directory path where the initial database files are stored.
        """
        self.apis_dir = apis_dir  # lv3_apis
        self.database_dir = database_dir # xx/api-bank/init_database
        
        self.apis = list()
        self.init_databases = dict()
        self.token_checker = None
        self.base_tools = dict() # the dict for LocalTool class before the initation
        self.tool2hash = dict()
        self.element_args: Dict[str, List] = dict() # Store the necessary args information for executing tools
        self.inited_tools: Dict[str, LocalTool] = dict()
        self.load_executable_tools()
        
    
    def load_executable_tools(self) -> None:
        """Loads executable tools from the specified directories.

        This method imports all Python files in the APIs directory, loads all classes,
        and initializes them if they are subclasses of API. It also loads initial databases
        from the database directory.

        Returns:
            None
        """
        

        init_database_dir = self.database_dir
        for file in os.listdir(init_database_dir):
            if file.endswith('.json'):
                database_name = file.split('.')[0]
                with open(os.path.join(init_database_dir, file), 'r') as f:
                    self.init_databases[database_name] = json.load(f)

        except_files = ['api']
        
        
        basename = "toolagent.apibank" + self.apis_dir
        package = __import__(basename, fromlist=['__path__'])
        package_path = package.__path__
        for _, subpackage_name, is_pkg in pkgutil.walk_packages(path=package_path, prefix=''):
            if subpackage_name not in except_files:
                
                module = importlib.import_module(f'{basename}.{subpackage_name}')
                
                classes = [getattr(module, x) for x in dir(module) if isinstance(getattr(module, x), type)]
                
                cls = classes[-1]
                if issubclass(cls, object) and cls is not object:
                    cls_info = {
                        'tool_name': cls.__name__,
                        'tool_description': cls.description,
                        'tool_set': "apibank",              
                        'input_parameters': cls.input_parameters,
                        'output_parameters': cls.output_parameters,
                        'executable': True,
                        'executable_type': "class",
                        'path': f'{basename}.{subpackage_name}',
                        'module_name': cls.__name__
                    }
                    
                    if hasattr(cls, 'database_name') and cls.database_name in self.init_databases:
                        cls_info['database'] = self.init_databases[cls.database_name]
                    
                    if cls_info["tool_name"] != "Toolsearcher":
                        base_tool = LocalTool(**cls_info)  
                        self.base_tools[base_tool.tool_id] = base_tool 
                        self.apis.append([cls_info["tool_name"], base_tool])
                        
                        
                    if cls_info["tool_name"] == "CheckToken":
                        self.token_checker =  self.init_tool(base_tool)

            
        for _, base_tool in self.apis:
            init_base_tool = self.init_tool(base_tool)
            self.inited_tools[base_tool.tool_id] = init_base_tool 
    

    def init_tool(self, base_tool: LocalTool, *args, **kwargs):
        """Initializes a tool with the given name and parameters.

        Parameters:
            tool_name (str): the name of the tool to initialize.
            args (list): the positional arguments to initialize the tool with.
            kwargs (dict): the parameters to initialize the tool with.

        Returns:
            tool (object): the initialized tool.
        """
       
        temp_args = []
    
        if base_tool.database:
            temp_args.append(base_tool.database)
        
        if base_tool.tool_name != 'CheckToken' and 'token' in base_tool.input_parameters:
            temp_args.append(self.token_checker)

        args = temp_args + list(args)
        
        self.element_args[base_tool.tool_id] = args
        
        base_tool.import_apply_args(*args, **kwargs)

        return base_tool
    
    def get_inited_tools(self):
        """Return the dictionary of executable tools.

        Returns:
            Dict[str, SysTool]: 
        """
        return self.inited_tools
    


class TooleyesLoader:
    def __init__(self, apis_dir: str) -> None:
        """Initialize the TooleyesLoader with the directory containing the APIs.

        Args:
            apis_dir (str): The directory path where the API tools are stored.
        """
        self.apis_dir = apis_dir # tooleyes/Tool_Library
        self.apis = list()
        self.inited_tools = dict()
        self.load_executable_tools()
        
    
    def load_executable_tools(self) -> None: #Tooleyes需要进行同名API排查
        """
        """

        basename = "toolagent.tooleyes"
        
        package = importlib.import_module(basename)
        package_path = package.__path__[0]


        for dirpath, _, filenames in os.walk(package_path):
            for filename in filenames:
                if filename == "config_gpt4.json":
                    full_path = os.path.join(dirpath, "filename")
                    tool_path = os.path.join(dirpath, "tool.py")
                    parts = tool_path.split('/')
                    try:
                        index = len(parts) - 1 - parts[::-1].index('toolagent')
                    except ValueError:
                        raise ValueError("The path can not be found")
                    import_path = '.'.join(parts[index:])
                    if import_path.endswith('.py'):
                        import_path = import_path[:-3]
                
                    with open(full_path, 'r') as file:
                        tools = json.load(file)
                    for tool in tools:
                        name = tool["name"]
                        if name not in ["ask_to_user", "finish"]:
                
                            cls_info = {
                                'tool_set': "Tooleyes",
                                'tool_name': name,
                                'tool_description': tool["description"],
                                'input_parameters': tool["parameters"]["properties"],
                                'output_parameters': None,
                                "required" : tool["parameters"]["required"],
                                'executable': True,
                                'executable_type': "function",
                                "path": import_path,
                                "module_name": name  
                            }
                            
                        base_tool = LocalTool(**cls_info)
                        self.apis.append([cls_info["tool_name"], base_tool])
                        self.inited_tools[base_tool.tool_id] = base_tool
                                       
    
    
    def get_inited_tools(self):
        """
        """
        return self.inited_tools
    



class TooltalkLoader:
    def __init__(self, init_database_dir: str, ignore_list: List = [], account_database: str = "Account") -> None:
        """
        """
        self.init_database_dir = init_database_dir
        self.ignore_list = ignore_list 
        self.account_database = account_database
        
        
        self.databases = dict()
        self.session_token = None
        self.now_timestamp = None
        self.apis = []
        self.base_tools = dict() # the dict for LocalTool class before the initation
        self.inited_tools = dict() #t he inited tools
        
        for file_name, file_path in self.get_names_and_paths(self.init_database_dir):
            database_name, ext = os.path.splitext(file_name)
            if ext == ".json":
                with open(file_path, 'r', encoding='utf-8') as reader:
                    self.databases[database_name] = json.load(reader)
        if self.account_database not in self.databases:
            raise ValueError(f"Account database {self.account_database} not found")
        
        self.load_executable_tools()


    def load_executable_tools(self) -> None:
        """
        """
        basename = "toolagent.tooltalk.apis"
        module_all = importlib.import_module(basename)
        ALL_APIS = getattr(module_all, "ALL_APIS")
        
        for cls in ALL_APIS:
            module_name = cls.__module__.split('.')[-1]
            path = basename + "." + module_name
            
            description = cls.description
            input_parameters = {}
            output_parameters = cls.output
            required = []
            for k, v in cls.parameters.items():
                if v["required"]:
                    required.append(k)
                del v["required"]
                input_parameters[k] = v
            
            cls_info = {
                    'tool_set': "Tooltalk",
                    'tool_name': cls.__name__,
                    'tool_description': description,
                    'input_parameters': input_parameters,
                    'output_parameters': output_parameters,
                    'required': required,
                    'executable': True,
                    'executable_type': "class",
                    'module_name': cls.__name__,
                    'path': path
                }
            if hasattr(cls, 'database_name') and cls.database_name in self.databases:
                cls_info['database'] = self.databases[cls.database_name]
            
            base_tool = LocalTool(**cls_info)
            self.base_tools[base_tool.tool_id] = base_tool 
            self.apis.append([cls_info["tool_name"], base_tool])
            
        
        for _, base_tool in self.apis:
            init_base_tool = self.init_tool(base_tool)
            self.inited_tools[base_tool.tool_id] = init_base_tool 
        
            
        

    def init_tool(self, base_tool: LocalTool):
        """
        """
        
        account_db = self.databases.get(self.account_database)
        if base_tool.database is not None:
            
            d = {"account_db": account_db, "now_timestamp": self.now_timestamp, "api_database": base_tool.database}
            base_tool.import_apply_args(**d)
        else:
            d = {"account_db": account_db, "now_timestamp": self.now_timestamp}
            base_tool.import_apply_args(**d)

        
        return base_tool
    
    def get_inited_tools(self):
        """
        """
        return self.inited_tools
    
    def get_names_and_paths(self, input_path):
        """
        """
        if os.path.isdir(input_path):
            files = os.listdir(input_path)
            file_paths = [os.path.join(input_path, name) for name in files]
            file_names_and_paths = [(name, path) for name, path in zip(files, file_paths)]
            return file_names_and_paths
        elif os.path.isfile(input_path):
            return [(os.path.basename(input_path), input_path)]
        else:
            raise ValueError(f"Unknown input path: {input_path}")
        
    
    def test(self, api_name, base_tool: LocalTool, parameters: Dict):
        request = {
            "api_name": api_name,
            "parameters": parameters
        }
        if api_name not in self.apis:
            response = {
                "response": None,
                "exception": f"API {api_name} not found"
            }
            return request, response

        tool = base_tool.init_func_module
        if tool.requires_auth:
            if self.session_token is None:
                response = {
                    "response": None,
                    "exception": "User is not logged in"
                }
                return request, response
            parameters["session_token"] = self.session_token
        if api_name in ["UserLogin", "RegisterUser"] and self.session_token is not None:
            username = tool.check_session_token(self.session_token)["username"]
            response = {
                "response": None,
                "exception": f"Only one user can be logged in at a time. Current user is {username}.",
            }
            return request, response

        # execute tool
        response = base_tool(**parameters)

        # capture session_token and simulate login and logout
        if api_name in ["UserLogin", "RegisterUser"] and response["exception"] is None:
            self.session_token = response["response"]["session_token"]
        elif api_name in ["LogoutUser", "DeleteAccount"] and response["exception"] is None:
            self.session_token = None
        return request, response
        