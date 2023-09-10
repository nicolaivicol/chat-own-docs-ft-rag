import os
from colorama import init, Fore, Style

from chat.chatobj import Chat

init(autoreset=True)

def chat_console():
    chat = Chat()

    while True:
        user_input_message = input("User: ")

        if user_input_message.lower() in ['exit', 'quit']:
            print("Assistant: Goodbye!")
            break

        chat.ask_gpt(user_input_message)
        docs = chat.get_titles_most_relevant_docs()
        if docs:
            docs = 'Servicii probabil relevante:\n' + '\n'.join([f' {i+1}) [{doc}]' for i, doc in enumerate(docs)])
            print(f"{Fore.LIGHTBLACK_EX}{docs}")
        assistant_answer = f"Assistant:{Fore.BLUE} {chat.last_answer_from_assistant}"
        print(assistant_answer)


if __name__ == "__main__":
    chat_console()
