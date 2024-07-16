# ToolAgent

## Usage

Basic

```python
import toolagent as ta

if __name__ == "__main__":
	agent = ta.Agent(model_checkpoint_path)
  
  agent.load_tool_module(embedding_checkpoint_path) #默认加载基于检索的工具模块
  agent.tool_module.load_tools(toolset_path) #加载工具集

  response = agent.chat(query)
  agent.clear_history()

```

Full

```python
import toolagent
from toolagent.agents import Agent

# 基座模型 & Embedding
from toolagent.model import AutoLLM
from toolagent.retrival.embedding import AutoEmbedding

# 三个模块
from toolagent.tools.calling import ToolCalling
from toolagent.data.document import DocRetriever #暂不实现
from toolagent.prompt.chat import ChatManager #可省略

# 评测pipeline
from toolagent.pipeline import EvalPipeline
from toolagent.data.dataset import Dataset

if __name__ == "__main__":
  ta.config
  ta.logger
 
  #加载所需模型
  model = AutoLLM(checkpoint_path_1) #本地权重或云端仓库或Server
  embedding = AutoEmbedding(checkpoint_path_2)
  
  # 核心类
	agent = Agent(model)
  
  #工具调用模块
  agent.tool_module = ToolCalling(embedding) #默认的工具调用模块 使用检索
  #agent.tool_module = ICLCalling(tool_prompt) 可使用其他工具调用模块，不检索
  agent.tool_module.load_tools(toolset_path)
 
	#可选：RAG模块（暂时不考虑实现）
	agent.RAG_module = DocRetriever(embedding) #RAG模块共享embedding，或额外定义
  agent.RAG_module.load_documents(library_path)
  
  #可选：对话管理模块(自动加载默认模块)，涉及对话模版、对话历史、System Prompt等等
  agent.chat_module = ChatManager() # 该步骤可省略，自动加载默认对话管理模块，仅作展示，方便用户自定义

  #应用：正常对话
  response = agent.chat(query)
  agent.clear_history() # 实质：agent.chat_module.clear_history()
  
  #应用：评测Pipeline
  eval_dataset = Dataset.from_path(dataset_path)
  result = EvalPipeline(agent, eval_dataset)
  
  

```

## Code Structure

```yaml
__init__: 初始化日志
_version: 版本信息
pipeline: 简易管线

agents/: 助手
	agent: 默认助手类

data/: 数据
	dataset: 数据集
	document/: 外部文档
		pool: 助手的RAG模块
		parse: 各种文档解析处理/切片等

tools/: 工具
	tool: 工具类
	calling: 助手的工具调用模块

model/: 模型
	LLM/: 大语言模型
	VLM/: 

prompt/:
	chat: 助手的对话管理模块

retrieval/: 检索
	retriever: 检索类，用于工具调用/RAG模块
	./embedding/: 词向量模型
	./vectorstore/: 检索向量库
```





