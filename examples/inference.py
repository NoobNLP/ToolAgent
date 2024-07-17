import toolagent as ta
from toolagent.agents import ReActAgent
from toolagent.retrieval import TopKRetriever

if __name__ == "__main__":
    tools = ta.load_tools("API-Bank", revision="level-1")
    retriever = TopKRetriever(tools, embedder="bge-small", vectorstore="ram", k=5)
    agent = ReActAgent(retriever=retriever)

    query = "Calculate 1 + 2"
    response = agent(query)
    print(response)
