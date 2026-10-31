from src.llm.model import llm
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

#response = llm.invoke("Explain what an ai agent is with customer support examples.")

# response = llm.invoke([
#     SystemMessage(content="You are a helpful and professional customer support assistant."),
#     HumanMessage(content="where is my order id 12345?")
# ])

prompt = ChatPromptTemplate.from_messages([
    ("system", "Act as a professional customer support assistant."),
    ("system", "Address the customer by name."),
    ("system", "Provide 1 line response."),
    ("system", "Never invent order status.."),
    ("human", "where is my order id {order_id}? and my name is {customer_name}")
])

messages = prompt.format_messages(order_id="12345",customer_name="John Doe")

response = llm.invoke(messages)

print("\nAI Response:")
print(response.content)