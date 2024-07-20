"""Main Agent Class

"""

from typing import Any

from toolagent.chat.prompt import ReActPromptSet

class ReAct_LLM_Agent:
    def __init__(
        self,
        name: str = "Agent",
        description: str = "A chat agent which is euipped with tool learning and RAG.",
        foundation_model = None,
        embedding_model = None,
        chat_module = None,
        tool_module = None,
        # rag_module= None,
    ) -> None:
        self.name = name
        self.description = description

        self.system_prompt = None

        self.foundation_model = foundation_model
        self.embedding_model = embedding_model

        self.chat_module = chat_module
        self.tool_module = tool_module
        # self.rag_module = rag_module

        if self.chat_module is None:
            self.load_chat_module()
        if self.tool_module is None:
            self.load_tool_module()

        self.chat_module.prompt_set = ReActPromptSet()

    def load_foundation_model(self) -> None:
        self.foundation_model = ...

    def load_model(self) -> None:
        self.load_foundation_model()

    def load_chat_module(self) -> None:
        self.chat_module = ...

    def load_tool_module(self) -> None:
        self.tool_module = ...

    def chat(self, query) -> Any:
        # Phase 1: Thought
        candidate_tool_list = self.tool_module.search_relevant_tools(query)
        prompt_1 = self.chat_module.get_prompt("Thought_prompt", [query,candidate_tool_list])
        raw_output_1 = self.foundation_model(prompt_1)
        output_1 = self.chat_module.process_prompt_response("Thought_prompt", raw_output_1)

        # Phase 2: Action
        tool = self.tool_module.judge_calling(candidate_tool_list, output_1)
        if tool is not None:
            # 工具调用的参数生成部分待补充
            calling_result = tool(parameters)
        else:
            return output_1
        
        # Phase 3: Observation
        prompt_2 = self.chat_module.get_prompt("Observation_prompt",[...])
        raw_output_2 = self.foundation_model(prompt_2)
        output_2 = self.chat_module.process_prompt_response("Observation_prompt", raw_output_2)
        return output_2

    def clear_history(self) -> None:
        self.chat_module.clear_history()

    def __call__(self, query) -> Any:
        return self.chat(query)
