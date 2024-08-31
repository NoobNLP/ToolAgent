from typing import Dict, Set, Tuple, List

from toolagent.types.proto import ToolProtocol

class RetrievableToolCallingModule:
    def __init__(self, embedder, retriever) -> None:
        self.toolpool: Dict[str, ToolProtocol] = dict() # 用tool_id作为key
        self.retriever = retriever(embedder)
        self.tool_prompt = f"Tool name: {1}, Tool description: {2}" #计算工具Embedding时使用

    def add_tool(self, tool: ToolProtocol, Check: bool=True) -> str:
        # 将工具添加到toolpool，用embedder计算embedding存储到embstore
        tool_id = tool.tool_id
        self.toolpool[tool.tool_id] = tool
        return tool_id

    def remove_tool(self, tool_id: str) -> None:
        del self.toolpool[tool_id]

    def add_tools(self, tool_set_path, check: bool=True): #从一个工具集批量导入工具
        #添加到toolpool，emb存储到retriever的embstore
        
        #仅以当前apibank示例(放的位置不对, 放在ToolAgent/tools/conert_api_bank_to_ta.py)
        from tools.conert_api_bank_to_ta import APIbankLoader
        instance = APIbankLoader(database_dir = "")
        apibank_tools = instance.get_inited_tools
        for tool in apibank_tools:
            self.toolpool[tool.tool_id] = tool

    def remove_tools(self,tool_set_name):
        #将tool_set相关工具从toolpool和embstore中移除

    def get_tools(self, tool_ids: str | List[str]): # 根据tool_id返回工具列表
        if isinstance(tool_ids, str):
            return self.toolpool[tool_ids]
        else:
            return [self.toolpool[tool_id] for tool_id in tool_ids]

    def check_duplication(self, tool: ToolProtocol) -> Tuple[bool, str]:
        #检查工具是否已在池中，是的话返回tool_id
        if tool.tool_id in self.toolpool:
            return True, tool.tool_id
        else:
            return False, None


    def search_relevant_tools(self, query) -> List:
        tool_id_list = self.retriever.retrieval(query)
        tool_list = self.get_tools(tool_id_list)
        return tool_list
    
    def judge_calling(candidate_tool_list: List, output_1) -> ToolProtocol: #根据agent.py设置
        pass