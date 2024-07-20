
from toolagent.data import load_dataset


class EvalPipeline:
    def __init__(self, agent, dataset_path):
        self.agent = agent
        self.dataset = load_dataset(dataset_path)
        self.infer_result = ...

    def inferrence(self): #推理数据集，将结果保存至self.infer_result
        ...

    def save_result(self, path): #将推理结果保存至指定目录
        ...

    def evaluation(self): #根据推理结果计算指标
        ... # 具体计算方式可以调用自.toolagent.utils.metrics