from typing import Literal
import heapq

import numpy as np

from retrieval.embstore import EmbStore

def top_k_keys_by_value(d, k):
    return [
        key for key, value in heapq.nlargest(k, d.items(), key=lambda item: item[1])
    ]

class Retriever:
    def __init__(self, embedder) -> None:
        self.top_k: int = 1
        self.similarity: Literal["cosine"] = "cosine"
        self.embedder = embedder
        self.embstore = EmbStore()

    def retrieval(self, query_vector) -> str:
        score_dict = dict()
        for key_id in self.embstore.storage:
            score_dict[key_id] = self.calculate_score(
                query_vector, self.embstore.storage[key_id]
            )
        return top_k_keys_by_value(score_dict, self.top_k)

    def calculate_score(self, vector_1, vector_2):
        match self.similarity:
            case "cosine":
                vec1 = np.array(vector_1)
                vec2 = np.array(vector_2)
                # 计算点积
                dot_product = np.dot(vec1, vec2)
                # 计算向量的模
                norm_vec1 = np.linalg.norm(vec1)
                norm_vec2 = np.linalg.norm(vec2)
                # 计算余弦相似度
                cosine_sim = dot_product / (norm_vec1 * norm_vec2)
                return cosine_sim