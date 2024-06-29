from zipfile import ZipFile
import logging
from typing import Optional, Any

from constants import *
from utils import user_select_from_list
from parser import Parser

LOGGER = logging.getLogger(__name__)


class ImportLib:

    def __init__(self, input_library_path: Optional[str] = "", library_source: Optional[str] = SOURCE_DEFAULT) -> None:

        # Initialise empty attributes
        self._input_library_path      = None # e.g. "../zipfiles/LIB_M24256X-FCU6T_VF.zip"
        self._input_library_extension = None # e.g. "zip"
        self._input_source            = None # e.g. "cse"

        self._imported_symbol    = None
        self._imported_footprint = None
        self._imported_model     = None

        self._output_symbol_name    = None
        self._output_footprint_name = None
        self._output_model_name     = None

        # Apply input values to attributes
        self.set_input_library(input_library_path)
        self.set_source(library_source)

    def set_input_library(self, input_library_path: str) -> None:
        self._input_library_path = input_library_path

        if self._input_library_path.count("."):
            self._input_library_extension = self._input_library_path.split(".")[-1] # TODO: Redo with handling for directories
        else:
            self._input_library_extension = None
        
    def set_source(self, library_source: str) -> None:
        """
        Source of the library
        """
        self._input_source = library_source

    def __import_zipped(self) -> None:
        LOGGER.info(f"Function 'import_cse_zipped' is WIP")

        symbols_found    = []
        footprints_found = []
        models_found     = []

        symbol_file_name    = None
        footprint_file_name = None
        model_file_name     = None

        with ZipFile(self._input_library_path, "r") as zipfile:

            for name in zipfile.namelist():
                extension = name.split(".")[-1] # TODO: Make sure split is successful

                if extension in SYMBOL_EXTENSIONS:
                    symbols_found.append(name)
                elif extension in FOOTPRINT_EXTENSIONS:
                    footprints_found.append(name)
                elif extension in MODEL_EXTENSIONS:
                    models_found.append(name)

            # Get symbol
            if symbols_found:
                symbol_file_name = user_select_from_list(symbols_found, "symbol file")
                LOGGER.info(f"Importing '{symbol_file_name}'")
                try:
                    with zipfile.open(symbol_file_name, "r") as symbol_file:
                        self._imported_symbol = symbol_file.read().decode("utf-8")
                except Exception as e:
                    # TODO: Change the line above to an approprate exception and handle properly
                    LOGGER.error(e)
                    exit(1)
            else:
                LOGGER.warning(f"No symbols found in library {self._library_path}")

            # Get footprint
            if footprints_found:
                footprint_file_name = user_select_from_list(footprints_found, "footprint file")
                LOGGER.info(f"Importing '{footprint_file_name}'")
                try:
                    with zipfile.open(footprint_file_name, "r") as footprint_file:
                        self._imported_footprint = footprint_file.read().decode("utf-8")
                except Exception as e:
                    # TODO: Change the line above to an approprate exception and handle properly
                    LOGGER.error(e)
                    exit(1)
            else:
                LOGGER.warning(f"No footprints found in library {self._library_path}")

            # Get model
            if models_found:
                model_file_name = user_select_from_list(models_found, "model file")
                LOGGER.info(f"Importing '{model_file_name}'")
                try:
                    with zipfile.open(model_file_name, "r") as model_file:
                        self._imported_model = model_file.read().decode("utf-8")
                except Exception as e:
                    # TODO: Change the line above to an approprate exception and handle properly
                    LOGGER.error(e)
                    exit(1)
            else:
                LOGGER.warning(f"No models found in library {self._library_path}")
    

    def __import(self) -> None:
        LOGGER.error(f"Function '__import' hasn't been implemented, exiting")
        exit(1)
    
    def __relink(self) -> None:
        """
        1. Set the symbol's footprint to the library name
        2. Set the footprint's model to the library name
        """

        LOGGER.warning(f"Function '__relink' is WIP")
        
        symbol_parser = Parser(self._imported_symbol)
        self._imported_symbol = symbol_parser.rename_node(node_type="property", old_node_name="\"Footprint\"", old_node_name_start_only=True, new_node_name=f"\"Footprint\" \"temp\"") # TODO: Change "temp"

        footprint_parser = Parser(self._imported_footprint)
        self._imported_footprint = footprint_parser.rename_node(node_type="model", old_node_name="", old_node_name_start_only=True, new_node_name="temp.stp")

    def import_single(self) -> None:
        """
        """
        
        if self._input_library_extension is None:
            self.__import()
        elif self._input_library_extension == "zip":
            self.__import_zipped()
        else:
            LOGGER.error(f"Unsupported library extension '.{self._input_library_extension}', exiting")
            exit(1)

        with open("symbol.txt", "w") as file:
            file.write(self._imported_symbol)

        self.__relink()

        with open("symbol_edited.txt", "w", newline='') as file:
            file.write(self._imported_symbol)

        with open("footprint_edited.txt", "w", newline='') as file:
            file.write(self._imported_footprint)

    def import_multi(self) -> None:
        LOGGER.error(f"Function 'import_multi' hasn't been implemented, exiting")
        exit(1)





# if self._input_source == SOURCE_CSE:
# elif self._input_source == SOURCE_EEC:
# elif self._input_source == SOURCE_SNAP:
# else:
#     LOGGER.error(f"Unsupported source '{self._input_source}', exiting")
#     exit(1)