import openai
import time

class Chatgpt:
    """ chatgpt

    the model chatgpt

    Attributes:
        model_name (str): model name
        openai_key (str): openai_key
        time : the start time
        TRY_TIME (int): max try times

    """
    def __init__(self, model_name: str="gpt-3.5-turbo-16k-0613", openai_key: str=""):
        self.model_name = model_name
        self.openai_key = openai_key
        self.time = time.time()
        self.TRY_TIME = 6

    def __call__(self, history: list):
        url = "https://api.openai.com/v1"
        OPENAI_API_KEY = ""
        openai.api_key = OPENAI_API_KEY
        openai.api_base = url
        response = openai.ChatCompletion.create(model=self.model_name, messages=history, stream=False)
        return response


