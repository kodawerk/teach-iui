import ollama

MODEL_NAME = 'llama3' 
SYSTEM_PROMPT = "You are a helpful and concise assistant. Keep your answers brief."
EXIT_COMMANDS = ['/quit', '/exit', '/bye']

def chat():
    try:
        # init clietn 
        client = ollama.Client()

        # create system prompt
        messages = [
            {
                'role': 'system',
                'content': SYSTEM_PROMPT,
            },
        ]

        print("\n")
        print("-" * 40)
        print(f"Model: {MODEL_NAME}")
        print(f"System Prompt: {SYSTEM_PROMPT}")
        print(f"Exit commands: {' or '.join(EXIT_COMMANDS)}")
        print("-" * 40)
        print("\n")

        # chat loop
        while True:
            user_input = input("You: ")

            # check for exit comands
            if user_input.lower() in EXIT_COMMANDS:
                print("bye")
                break

            # append new user message to history
            messages.append({
                'role': 'user',
                'content': user_input,
            })

            print("Ollama: ", end='', flush=True)
            
            # stream response
            stream = client.chat(
                model=MODEL_NAME,
                messages=messages,
                stream=True
            )

            full_response = ""
            for chunk in stream:
                content = chunk['message']['content']
                print(content, end='', flush=True)
                full_response += content
            
            # new line
            print()

            # add response to history
            messages.append({
                'role': 'assistant',
                'content': full_response,
            })
            
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    chat()