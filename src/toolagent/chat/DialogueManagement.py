
class DialogueManagement:
    def __init__(self):
        self.prompt_set = None
        self.chat_history = []

    def clear_history(self):
        self.chat_history = []

    def get_prompt(self, prompt_name, values) -> str:
        return self.prompt_set(prompt_name, values)

    def process_prompt_result(self, prompt_name, text) -> str:
        ...