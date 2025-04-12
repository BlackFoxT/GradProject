from langchain_community.llms.ollama import Ollama

# Initialize Ollama model
llm = Ollama(model="llama3.2")

# Optionally, you can also define a function to invoke the model:
def invoke_message(message):
    response = llm.invoke(message)
    return response
