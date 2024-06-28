from zipfile import ZipFile
import logging
from typing import Optional, Any

from constants import *
from utils import user_select_from_list

LOGGER = logging.getLogger(__name__)




class ImportLib:

    def __init__(self, input_library_path: Optional[str] = "", library_source: Optional[str] = SOURCE_DEFAULT) -> None:

        # Initialise empty attributes
        self._library_path = None # e.g. "Downloads/LIB_M24256X-FCU6T_VF.zip"
        self._library = None # e.g. "LIB_M24256X-FCU6T_VF.zip"
        self._library_extension = None # e.g. "zip"
        self._library_name = None # e.g. "LIB_M24256X-FCU6T_VF"
        self._source = None
        self._imported_symbol = None
        self._imported_footprint = None
        self._imported_model = None

        # Apply input values to attributes
        self.set_input_lib(input_library_path)
        self.set_source(library_source)

    def set_input_lib(self, input_library_path: str) -> None:
        self._library_path = input_library_path
        self._library = input_library_path.split("/")[-1].split("\\")[-1]
        self._library_extension = self._library.split(".")[-1] # TODO: Redo with handling for directories
        self._library_name = self._library.split(".")[0]

    def set_source(self, library_source: str) -> None:
        self._source = library_source

    def __import_zipped(self) -> None:
        LOGGER.info(f"Function 'import_cse_zipped' is WIP")

        symbols_found = []
        footprints_found = []
        models_found = []

        symbol_file_name = None
        footprint_file_name = None
        model_file_name = None

        with ZipFile(self._library_path, "r") as zipfile:

            for name in zipfile.namelist():
                extension = name.split(".")[-1] # TODO: Make sure split is successful

                if extension == SYMBOL_EXTENSION:
                    symbols_found.append(name)
                elif extension == FOOTPRINT_EXTENSION:
                    footprints_found.append(name)
                elif extension == MODEL_EXTENSION:
                    models_found.append(name)
            
            # Get symbol
            if symbols_found:
                symbol_file_name = user_select_from_list(symbols_found, "symbol file")
                LOGGER.info(f"Importing '{symbol_file_name}'")
                try:
                    with zipfile.open(symbol_file_name, "r") as symbol_file:
                        self._imported_symbol = symbol_file.read()
                except Exception as e:
                    # TODO: Change the line above to an approprate exception and handle properly
                    LOGGER.error(e)
                    exit(1)
            else:
                LOGGER.warning(f"No symbols found in library {self._library}")

            # Get footprint
            if footprints_found:
                footprint_file_name = user_select_from_list(footprints_found, "footprint file")
                LOGGER.info(f"Importing '{footprint_file_name}'")
                try:
                    with zipfile.open(footprint_file_name, "r") as footprint_file:
                        self._imported_footprint = footprint_file.read()
                except Exception as e:
                    # TODO: Change the line above to an approprate exception and handle properly
                    LOGGER.error(e)
                    exit(1)
            else:
                LOGGER.warning(f"No footprints found in library {self._library}")

            # Get model
            if models_found:
                model_file_name = user_select_from_list(models_found, "model file")
                LOGGER.info(f"Importing '{model_file_name}'")
                try:
                    with zipfile.open(model_file_name, "r") as model_file:
                        self._imported_model = model_file.read()
                except Exception as e:
                    # TODO: Change the line above to an approprate exception and handle properly
                    LOGGER.error(e)
                    exit(1)
            else:
                LOGGER.warning(f"No models found in library {self._library}")
    

    def __import(self) -> None:
        LOGGER.error(f"Function '__import' hasn't been implemented, exiting")
        exit(1)
    
    def __relink(self) -> None:
        """
        1. Set the symbol's footprint to the library name
        2. Set the footprint's model to the library name
        """

        LOGGER.error(f"Function '__relink' hasn't been implemented, exiting")
        exit(1)


    def import_single(self) -> None:
        """
        """
        
        if self._library_extension == "zip":
            self.__import_zipped()
        else:
            self.__import()

        self.__relink()

    def import_multi(self) -> None:
        LOGGER.error(f"Function 'import_multi' hasn't been implemented, exiting")
        exit(1)





# if self._source == SOURCE_CSE:
# elif self._source == SOURCE_EEC:
# elif self._source == SOURCE_SNAP:
# else:
#     LOGGER.error(f"Unsupported source '{self._source}', exiting")
#     exit(1)