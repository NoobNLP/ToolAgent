from toolagent.chat.prompt import ReActPromptSet
import re
import json
class DialogueManagement:
    """ Dialogue management
    管理对话，获得prompt，同时存储历史信息

    Attributes:
        prompt_set : the function used to get prompt according to candidate tools and so on.
        chat_history (list): the history of the chat.

    """
    def __init__(self):
        self.prompt_set = None
        self.chat_history = []

    def clear_history(self)->None:
        """ clear history data

        clear history information

        """
        self.chat_history = []

    def get_prompt(self, prompt_name: str, values: dict) -> str:
        """ get prompt

        读取prompt

        Args:
            prompt_name (str): your prompt name
            values (dict): the candidate information such as candidate tools or something else

        Returns:
            str: final prompt

        """
        return self.prompt_set(prompt_name, values)

    def process_prompt_result(self, prompt_name: str, text: str):
        """ process model output

        process model output

        Args:
            prompt_name (str): the type of prompt
            text (str): model response


        """
        if prompt_name == "Thought_prompt":
            used_tools = re.search("\[[\s\S]*\]", text)
            if used_tools != None:
                used_tools = used_tools.group(0)
            else:
                return []
            try:
                tools = json.loads(used_tools)
            except:
                print("the format of model's response is wrong")
                tools = []

            return tools
        else:
            return text


    def add_message(self, message: dict)->None:
        """ add message

        将新生成的信息加入到历史信息中

        Args:
            message (dict): new message

        Returns:
            None

        """
        self.chat_history.append(message)




