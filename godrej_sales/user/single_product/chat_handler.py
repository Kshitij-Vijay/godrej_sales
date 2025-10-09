def handle_chat():
    from chat import llm_chain
    chain = llm_chain()
    conversation = converse(chain=chain)
    store_conversation(conversation)
    from create import re_analyse
    re_analyse()



def converse(chain):
    conversation = ""
    des = chain.run("give me a brief description of the product")
    print(des+"\n")
    while True:
        q = input("Enter query, [type 'exit' to quit] : ")
        if q=="exit":
            break
        else: 
            ans = chain.run(q)
            conversation = conversation + "Q: " + q + "\nA: " + ans + "\n \n"
            print(ans)
    return conversation

import os
import shutil

def store_conversation(text):
    chat_folder = os.path.join('extracted_data', 'chat')
    if not os.path.exists(chat_folder):
        os.makedirs(chat_folder)  # Create the chat folder if missing
        print(f"Created folder: {chat_folder}")

    files = [f for f in os.listdir(chat_folder) if f.endswith('.txt') and f[:-4].isdigit()]
    numbers = sorted([int(f[:-4]) for f in files])

    if numbers:
        new_number = numbers[-1] + 1
    else:
        new_number = 1

    new_file_path = os.path.join(chat_folder, f'{new_number}.txt')
    with open(new_file_path, 'w') as f:
        f.write(text)

    print(f"Stored conversation in {new_file_path}")




