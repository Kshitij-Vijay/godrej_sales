def ask_for_input_type():
    options = ["pdf", "webpage", "images"]
    print("Select data input type:")
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    choice = input("Enter number: ").strip()
    idx = int(choice) - 1
    return options[idx]
