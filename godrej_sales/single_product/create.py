from input_selector import ask_for_input_type

def raw_data():
    input_type = ask_for_input_type()
    if input_type == "pdf":
        from pdf_handler import handle_pdf
        handle_pdf()
    if input_type == "webpage":
        from url_handler import handle_url
        handle_url()
    else:
        print("Other input types (webpage, images) not yet implemented.")

def create():
    t = input("Do you want to add data ? (y/n) \n")
    if(t=='y'):
        raw_data()
        create()
        

