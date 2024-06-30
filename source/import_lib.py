from zipfile import ZipFile
import logging
from typing import Optional, Any

from constants import *
from utils import user_select_from_list
from kiparser import KiParser

LOGGER = logging.getLogger(__name__)


class ImportLib:

    def __init__(self, input_library_path: Optional[str] = "",
                 library_source:           Optional[str] = SOURCE_DEFAULT,
                 symbol_name:              Optional[str] = "",
                 footprint_name:           Optional[str] = "",
                 model_name:               Optional[str] = "") -> None:
        """
        """

        # Initialise empty attributes
        self._input_library_path      = str() # e.g. "../zipfiles/LIB_M24256X-FCU6T_VF.zip"
        self._input_library_name      = str()
        self._input_library_extension = str() # e.g. "zip"
        self._input_source            = str() # e.g. "cse"
        self._input_model_extension   = str()

        self._symbol    = str()
        self._footprint = str()
        self._model     = str()

        self._output_symbol_name    = str()
        self._output_footprint_name = str()
        self._output_model_name     = str()

        # Apply input values to attributes
        self.set_symbol_name(symbol_name)
        self.set_footprint_name(footprint_name)
        self.set_model_name(model_name)
        self.set_input_library(input_library_path, library_source)

    def set_input_library(self, input_library_path: str, library_source: str, force_set_names: Optional[bool] = False) -> None:
        """
        force_set_names sets the symbol, footprint and model names to the library name, even if already set
        """
        
        self._input_library_path = input_library_path
        self._input_source = library_source

        if self._input_library_path.count("."):
            self._input_library_extension = self._input_library_path.split(".")[-1] # TODO: Redo with handling for directories
        else:
            self._input_library_extension = None

        # Set self._input_library_name
        if self._input_source == SOURCE_CSE:
            self._input_library_name = self._input_library_path.split("LIB_")[-1].split(".")[(-2 if self._input_library_extension is not None else -1)].replace(" ", "_")
        elif self._input_source == SOURCE_EEC:
            LOGGER.error(f"WRITE THIS CODE, exiting") # TODO
            exit(1)
        elif self._input_source == SOURCE_SNAP:
            LOGGER.error(f"WRITE THIS CODE, exiting") # TODO
            exit(1)
        else:
            LOGGER.error(f"Unsupported source '{self._input_source}', exiting")
            exit(1)

        # Set symbol name if required
        if not self._output_symbol_name or force_set_names:
            self.set_symbol_name(self._input_library_name)

        # Set footprint name if required
        if not self._output_footprint_name or force_set_names:
            self.set_footprint_name(self._input_library_name)

        # Set model name if required
        if not self._output_model_name or force_set_names:
            self.set_model_name(self._input_library_name)

    def set_symbol_name(self, symbol_name: str) -> None:
        """
        """
        self._output_symbol_name = symbol_name

    def set_footprint_name(self, footprint_name: str) -> None:
        """
        """
        self._output_footprint_name = footprint_name

    def set_model_name(self, model_name: str) -> None:
        """
        """
        self._output_model_name = model_name

    def __import_zipped(self) -> None:
        LOGGER.info(f"Function 'import_cse_zipped' is WIP")

        symbols_found    = []
        footprints_found = []
        models_found     = []

        with ZipFile(self._input_library_path, "r") as zipfile:

            for name in zipfile.namelist():
                extension = name.split(".")[-1] if name.count(".") else "invalid"

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
                        self._symbol = symbol_file.read().decode(ENCODING)
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
                        self._footprint = footprint_file.read().decode(ENCODING)
                except Exception as e:
                    # TODO: Change the line above to an approprate exception and handle properly
                    LOGGER.error(e)
                    exit(1)
            else:
                LOGGER.warning(f"No footprints found in library {self._library_path}")

            # Get model
            if models_found:
                model_file_name = user_select_from_list(models_found, "model file")
                self._input_model_extension = model_file_name.split(".")[-1]
                LOGGER.info(f"Importing '{model_file_name}'")
                try:
                    with zipfile.open(model_file_name, "r") as model_file:
                        self._model = model_file.read().decode(ENCODING)
                except Exception as e:
                    # TODO: Change the line above to an approprate exception and handle properly
                    LOGGER.error(e)
                    exit(1)
            else:
                LOGGER.warning(f"No models found in library {self._library_path}")
    

    def __import(self) -> None:
        LOGGER.error(f"Function '__import' hasn't been implemented, exiting")
        exit(1)
    
    def __relink_symbol_footprint(self) -> None:
        """
        Link the symbol to the footprint
        """

        symbol_parser = KiParser(self._symbol)
        self._symbol = symbol_parser.rename_node("property \"Footprint\"", f"\"{self._output_footprint_name}.kicad_mod\"") # TODO: Add output library

    def __relink_footprint_model(self) -> None:
        """
        Link the footprint to the model
        """

        footprint_parser = KiParser(self._footprint)
        self._footprint = footprint_parser.rename_node("model", f"{self._output_model_name}.{self._input_model_extension}") # TODO: Change "temp.stp"

    def write_symbol_file(self):
        """
        """
        # TODO: Add path to output
        with open(f"{self._output_symbol_name}.kicad_sym", "w", newline='') as file:
            file.write(self._symbol)

    def write_footprint_file(self):
        """
        """
        # TODO: Add path to output
        with open(f"{self._output_footprint_name}.kicad_mod", "w", newline='') as file:
            file.write(self._footprint)

    def write_model_file(self):
        """
        """
        # TODO: Add path to output
        with open(f"{self._output_model_name}.{self._input_model_extension}", "w", newline='') as file:
            file.write(self._model)

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

        if self._symbol and self._footprint:
            self.__relink_symbol_footprint()

        if self._footprint and self._model:
            self.__relink_footprint_model()


        self.write_symbol_file()
        self.write_footprint_file()
        self.write_model_file()

    def import_multi(self) -> None:
        LOGGER.error(f"Function 'import_multi' hasn't been implemented, exiting")
        exit(1)





# if self._input_source == SOURCE_CSE:
# elif self._input_source == SOURCE_EEC:
# elif self._input_source == SOURCE_SNAP:
# else:
#     LOGGER.error(f"Unsupported source '{self._input_source}', exiting")
#     exit(1)