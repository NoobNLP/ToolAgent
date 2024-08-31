"""Main Agent Class

"""

from typing import Any

from toolagent.chat.prompt import ReActPromptSet
from toolagent.chat.DialogueManagement import DialogueManagement
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

    def load_foundation_model(self, llm) -> None:
        """ load foundation mode

        load the model we use

        Args:
            llm :

        """
        self.foundation_model = llm

    def load_model(self, llm) -> None:
        self.load_foundation_model(llm)

    def load_chat_module(self) -> None:
        self.chat_module = DialogueManagement()

    def load_tool_module(self) -> None:
        self.tool_module = ...

    def chat(self, query, circle=1) -> Any:
        # Phase 1: Thought
        # candidate_tools = self.tool_module.search_relevant_tools(query)
        candidate_tools = []
        prompt_1 = self.chat_module.get_prompt("Thought_prompt", {"candidate_tools": candidate_tools})
        messages = [{"role": "system", "content": prompt_1}, {"role": "user", "content": query}]
        
        
        for i in range(circle):
            messages.extend(self.chat_module.chat_history)
            raw_output_1 = self.foundation_model(messages)
            output_1 = self.chat_module.process_prompt_result("Thought_prompt", raw_output_1)

            # Phase 2: Action
            # tool = self.tool_module.judge_calling(candidate_tool_list, output_1)
            # if tool is not None:
            #     # 工具调用的参数生成部分待补充
            #     parameters = output_1["parameters"]
            #     calling_result = tool(parameters)
            # else:
            #     return output_1
            


            # Phase 3: Observation
            self.chat_module.add_message({"role": "assistant", "content": raw_output_1})
            chat_history = self.chat_module.chat_history
            observation_information = {"chat_history": chat_history, "query": query}
            prompt_2 = self.chat_module.get_prompt("Observation_prompt", observation_information)
            messages_observation = [{"role": "system", "content": prompt_2}]
            raw_output_2 = self.foundation_model(messages_observation)
            output_2 = self.chat_module.process_prompt_result("Observation_prompt", raw_output_2)
            

        return output_2

    def clear_history(self) -> None:
        self.chat_module.clear_history()

    def __call__(self, query) -> Any:
        return self.chat(query)
