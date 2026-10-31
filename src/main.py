from src.llm.model import llm

response = llm.invoke("Explain what an ai agent is with customer support examples.")

print("\nAI Response:")
print(response.content)