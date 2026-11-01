import uuid

from src.agent import build_agent


def main():
    customer_name = input("Enter your name: ").strip() or "there"
    agent = build_agent(customer_name)
    
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    
    print("Type to 'exit' to quit.\n")
    
    while(True):
        user_input = input(f"{customer_name}: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        try:
            result = agent.invoke({
                "messages": [
                    {"role": "user", "content":user_input}
                ]},config,)

        except Exception as e:
            print(f"AI: Sorry, something went wrong. ({e})\n")
            continue
        
        messages = result["messages"]
        last_human = max(i for i, m in enumerate(messages) if m.type == "human")
        for msg in messages[last_human:]:
            for call in getattr(msg, "tool_calls", None) or []:
                    print(f"AI (tool call): {call['name']}({call['args']})\n")
                    
        print("AI: " + result["messages"][-1].content + "\n")
        # pprint(result)
        
if __name__ == "__main__":
    main()