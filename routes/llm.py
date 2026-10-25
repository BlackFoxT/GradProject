
"""
from langchain_community.llms.ollama import Ollama

# Initialize Ollama model
llm = Ollama(model="deepseek-r1:1.5b")

# Invoke the model:
def invoke_message(message):
    response = llm.invoke(message)
    
    return response
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# FH Aachen KI:connect (OpenAI-compatible API)
_client = OpenAI(
    base_url=os.environ["LLM_BASE_URL"],
    api_key=os.environ["LLM_API_KEY"],
    timeout=60,
)
_MODEL = os.environ["LLM_MODEL"]


class FHLLM:
    """Drop-in replacement for the old Ollama object: llm.invoke(text) -> str"""

    def invoke(self, message: str) -> str:
        result = _client.chat.completions.create(
            model=_MODEL,
            messages=[{"role": "user", "content": message}],
        )
        return result.choices[0].message.content or ""


llm = FHLLM()


def invoke_message(message):
    return llm.invoke(message)