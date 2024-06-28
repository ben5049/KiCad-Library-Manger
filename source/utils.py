from typing import List

def user_select_from_list(items: List[str], items_type: str) -> str:
    
    selection = 0 # Default selection is first item
    
    if not items:
        # TODO: Print error message
        return ""
    
    elif len(items) > 1:

        print(f"\n")
        for i, item in enumerate(items):
            print(f"{i}. {item}")
        print(f"Choose a {items_type} from the list above")

        user_input = input().strip()

        try:
            selection = int(user_input)
        except ValueError:
            LOGGER.warning(f"Invalid input '{user_input}', defaulting to first item")

    return items[selection]