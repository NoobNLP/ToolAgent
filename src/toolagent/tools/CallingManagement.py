from typing import Dict, Set, Tuple, List

from toolagent.types.proto import ToolProtocol

class RetrievableToolCallingModule:
    def __init__(self, embedder, retriever) -> None:
        self.toolpool: Dict[str, ToolProtocol] = dict() # 用tool_id作为key
        self.retriever = retriever(embedder)
        self.tool_prompt = ... #计算工具Embedding时使用

    def add_tool(self, tool: ToolProtocol, Check: bool=True) -> str:
        # 将工具添加到toolpool，用embedder计算embedding存储到embstore
        return tool_id

    def remove_tool(self, tool_id: str) -> None:
        ...

    def add_tools(self, tool_set_path, check: bool=True): #从一个工具集批量导入工具
        ...#添加到toolpool，emb存储到retriever的embstore

    def remove_tools(self,tool_set_name):
        ... #将tool_set相关工具从toolpool和embstore中移除

    def get_tools(self, tool_ids: str | List[str]): # 根据tool_id返回工具列表
        ...

    def check_duplication(self, tool: ToolProtocol) -> Tuple[bool, str]:
        ... #检查工具是否已在池中，是的话返回tool_id


    def search_relevant_tools(self, query) -> List:
        tool_id_list = self.retriever.retrieval(query)
        tool_list = self.get_tools(tool_id_list)
        return tool_list