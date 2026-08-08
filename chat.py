from agent import run_agent


def main():
    print("Expense Agent — type 'exit' to quit")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        print("Agent:", run_agent(user_input))


if __name__ == "__main__":
    main()