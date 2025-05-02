from langchain_community.llms.ollama import Ollama

# Initialize Ollama model
llm = Ollama(model="deepseek-r1:7b")

# Invoke the model:
def invoke_message(message):
    response = llm.invoke(message)
    
    return response

