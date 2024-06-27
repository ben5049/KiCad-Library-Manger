from typing import Any
import logging
import argparse

from constants import *
from import_lib import ImportLib


LOGGER = logging.getLogger(__name__)

class Klm:

    def __init__(self, args: Any) -> None:

        self.action = args.action

        # Composition
        self.importer = ImportLib(args.input)


    def __del__(self) -> None:
        pass

    def run(self) -> None:

        if self.action == ACTION_IMPORT:
            self.importer.import_single()
        
        else:
            pass



def parse_args() -> Any:
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("action",
                        action="store",
                        nargs=1,
                        default=None,
                        type=str,
                        choices=ACTION_LIST,
                        required=True,
                        help="Action to execute",
                        dest="action")
    
    parser.add_argument("-i",
                        "--input",
                        action="store",
                        default=None,
                        type=str,
                        required=False,
                        help="Library to import. Can be \".zip\" or a directory",
                        dest="input")
    
    parser.add_argument("-s",
                        "--source",
                        action="store",
                        default=SOURCE_DEFAULT,
                        type=str,
                        choices=SOURCE_LIST,
                        required=False,
                        help="Source of library",
                        dest="source")

    args = parser.parse_args()

    # Check if optional arguments are required

    return args


if __name__ == "__main__":
    
    args = parse_args()

    klm = Klm(args)
    klm.run()