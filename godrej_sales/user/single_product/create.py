def ask_for_input_type():
    options = ["pdf", "webpage", "images", "chat", "text"]
    print("Select data input type:")
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    choice = input("Enter number: ").strip()
    idx = int(choice) - 1
    return options[idx]

import os
import shutil

def delete_summaries():
        folders = ['summaries']
        for folder in folders:
            if os.path.exists(folder) and os.path.isdir(folder):
                shutil.rmtree(folder)
                print(f"Deleted folder: {folder}")
            else:
                print(f"Folder not found: {folder}")

def re_analyse():
    # only deletes summaries and again analyses extracted data. for chat bot input
    delete_summaries()
    from analyser.analyse import analyseee
    from embeddings import store_embeds
    analyseee()
    store_embeds()

def raw_data():
    input_type = ask_for_input_type()
    if input_type == "pdf":
        from pdf_handler import handle_pdf
        handle_pdf()
    if input_type == "webpage":
        from url_handler import handle_url
        handle_url()
    if input_type == "chat":
        from chat_handler import handle_chat
        handle_chat()
    if input_type == "text":
        from chat_handler import handle_text
        handle_text()
    else:
        print("Other input types (webpage, images) not yet implemented.")

def create():
    t = input("Do you want to add data ? (y/n) \n")
    if(t=='y'):
        raw_data()
        create()
        

