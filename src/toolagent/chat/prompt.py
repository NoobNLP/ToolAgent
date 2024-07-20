
class ReActPromptSet:
    def __init__(self):
        self.prompt_set = {
            "Thought_prompt": ...,
            "Observation_prompt": ... # TODO 需要在这都写好
        }

    def __call__(self, prompt_name: str, values: list) -> str:
        #可能需要对values列表进行处理，比如里面包含工具类
        return self.prompt_set[prompt_name].format(values)