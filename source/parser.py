import re
from typing import Optional

class Parser:

    def __init__(self, file: str) -> None:
        self._file = file
    
    def remove_empty_lines(self) -> str:

        new_file = ""

        for line in self._file.split("\n"):
            if line.strip():
                new_file += line + "\n"

        self._file = new_file

        return self._file

    def rename_node(self, node_type: str, old_node_name: str, new_node_name: str, old_node_name_start_only: Optional[bool] = False) -> str:
        
        pattern = node_type + " " + old_node_name + (r"\s*[^()]*?(?=\s*[()])" if old_node_name_start_only else "")
        replacement = node_type + " " + new_node_name

        self._file = re.sub(pattern, replacement, self._file, flags=re.MULTILINE)

        return self._file