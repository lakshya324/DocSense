# Using LLAMA 3 8B model (Langchain)
# Running on Ollama (Locally)

from langchain_community.llms import Ollama


def llama3(prompt: str) -> str:
    # LLAMA 3 8B model
    llm = Ollama(model="llama3")
    return llm.invoke(prompt)
