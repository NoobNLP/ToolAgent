from typing import List,Any

class HuggingFaceEmbedder:
    def __init__(self, checkpoint_path) -> None:
        from transformers import AutoModel, AutoTokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)
        self.model = AutoModel.from_pretrained(checkpoint_path, trust_remote_code=True)

    def __call__(self, inputs: str | List[str]) -> Any:
        batch_dict = self.tokenizer(inputs, padding=True, truncation=True, return_tensors='pt')
        outputs = self.model(**batch_dict)
        embeddings = outputs.last_hidden_state[:, 0]
        embedding_list = [sub_embedding.tolist() for sub_embedding in embeddings]
        return embedding_list #TODO 自定义embedding格式