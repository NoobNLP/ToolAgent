import toolagent as ta
from toolagent.agents import ReActAgent
from toolagent.models import LocalModel
from toolagent.retrieval import TopKRetriever

if __name__ == "__main__":
    tools = ta.load_tools("API-Bank", revision="level-1")
    retriever = TopKRetriever(embedder="bge-small", vectorstore="ram", k=5)
    llm = LocalModel("meta-llama/llama-3-8b-instruct")
    agent = ReActAgent(model=llm, tools=tools, retriever=retriever)

    query = "Calculate 1 + 2"
    response = agent(query)
    print(response)
