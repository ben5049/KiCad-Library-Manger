from typing import List
import logging

LOGGER = logging.getLogger(__name__)

def user_select_from_list(items: List[str], items_type: str) -> str:
    
    selection = 0 # Default selection is first item
    
    if not items:
        # TODO: Print error message
        return ""
    
    elif len(items) > 1:

        # Print options
        print(f"\n")
        for i, item in enumerate(items):
            print(f"[{i + 1}]\t{item}")
        print(f"Choose a {items_type} from the list above (1 to {len(items)}) ")

        # Get user input
        user_input = input().strip()

        # Make sure input is an integer
        try:
            selection = int(user_input) - 1
        except ValueError:
            LOGGER.warning(f"Invalid input '{user_input}', defaulting to first item")
        
        # Make sure input is in allowed range
        if (selection < 0) or (selection >= len(items)):
            LOGGER.warning(f"Invalid selection '{selection + 1}'. Defaulting to first item")
            selection = 0

    return items[selection]