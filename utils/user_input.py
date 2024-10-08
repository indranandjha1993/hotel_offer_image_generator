from typing import List, Any


def get_user_choice(prompt: str, options: List[Any], default: Any) -> Any:
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    while True:
        choice = input(
            f"Enter your choice (number) or press Enter for default ({default}): "
        ).strip()
        if choice == "":
            return default
        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(options):
                return options[choice_index]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or press Enter for default.")
