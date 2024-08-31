from transformers import AutoTokenizer, AutoModelForCausalLM

class LLaMA3:
    """LLaMA

    the LLaMA model

    Attributes:
        model_name (str):
        tokenizer: model tokenizer
        llm: the candidate model
        checkpoint_path (str): model parameters path

    """
    def __init__(self, checkpoint_path: str) -> None:
        self.model_name = 'LLaMA'

        self.checkpoint_path = checkpoint_path

        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint_path, trust_remote_code=True)
        self.llm = AutoModelForCausalLM.from_pretrained(self.checkpoint_path, trust_remote_code=True, device_map="auto") # torch_dtype=torch.bfloat16,
        self.llm.eval()


    def __call__(self, messages: list, max_new_length: int=256) -> str:
        input_text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        inputs = self.tokenizer(input_text, return_tensors="pt")
        try:
            generate_ids = self.llm.generate(inputs.input_ids.cuda(), max_new_tokens=max_new_length)

            outputs = self.tokenizer.decode(generate_ids[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True)
            return outputs
        except:
            pass


class Qwen:
    """Qwen

        the Qwen model

        Attributes:
            model_name (str):
            tokenizer: model tokenizer
            llm: the candidate model
            checkpoint_path (str): model parameters path

        """
    def __init__(self, checkpoint_path: str) -> None:
        self.model_name = 'Qwen'

        self.checkpoint_path = checkpoint_path

        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint_path, trust_remote_code=True)
        self.llm = AutoModelForCausalLM.from_pretrained(self.checkpoint_path, trust_remote_code=True, device_map="auto") # torch_dtype=torch.bfloat16,
        self.llm.eval()


    def __call__(self, input_text: str, max_new_length: int=256) -> str:
        inputs = self.tokenizer(input_text, return_tensors="pt")
        try:
            generate_ids = self.llm.generate(inputs.input_ids.cuda(), max_new_tokens=max_new_length)

            outputs = self.tokenizer.decode(generate_ids[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True)
            return outputs
        except:
            pass

