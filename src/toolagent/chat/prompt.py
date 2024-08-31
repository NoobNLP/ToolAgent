
class ReActPromptSet:
    def __init__(self):
        self.prompt_set = {
            "Thought_prompt": "You are a helpful assistant, you need to choose the suitable tool to complete the task based on user needs. Here are descriptions of the candidate tools' information. \nTool description: \n {candidate_tools}",
            "Observation_prompt": "You need to analyze and summarize historical tool calls based on user's query\n user: {query}\nchat_history:{chat_history}" # TODO 需要在这都写好
        }

    def __call__(self, prompt_name: str, values: dict) -> str:
        #可能需要对values列表进行处理，比如里面包含工具类
        if prompt_name == "Thought_prompt":
            candidate_tools = values["candidate_tools"]
            return self.prompt_set["Thought_prompt"].format(candidate_tools=candidate_tools)
        else:
            query = values["query"]
            chat_history = values["chat_history"]
            return self.prompt_set["Observation_prompt"].format(query=query, chat_history=chat_history)