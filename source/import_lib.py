from zipfile import ZipFile
import logging
from typing import Optional

from constants import *

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

    def __import_cse_zipped(self) -> None:
        LOGGER.info(f"Function 'import_cse_zipped' is WIP")

        symbol_path = self._library_name + "/KiCad/" + self._library_name + ".kicad_sym"
        
        footprint_path = "" # TODO: Search for ".kicad_mod" file extension

        model_path = self._library_name + "/3D/" + self._library_name + ".stp"

        with ZipFile(self._library_path, "r") as zipfile:

            # Get symbol
            try:
                with zipfile.open(symbol_path, "r") as symbol_file:
                    self._imported_symbol = symbol_file.read()
            except Exception as e:
                # TODO: Change the line above to an approprate exception and handle properly
                LOGGER.error(e)
                exit(1)

            # Get footprint
            try:
                with zipfile.open(footprint_path, "r") as footprint_file:
                    self._imported_footprint = footprint_file.read()
            except Exception as e:
                # TODO: Change the line above to an approprate exception and handle properly
                LOGGER.error(e)
                exit(1)

            # Get model
            try:
                with zipfile.open(model_path, "r") as model_file:
                    self._imported_model = model_file.read()
            except Exception as e:
                # TODO: Change the line above to an approprate exception and handle properly
                LOGGER.error(e)
                exit(1)

    def __import_cse(self) -> None:

        if self._library_extension == "zip":
            self.__import_cse_zipped()
        else:
            LOGGER.error(f"Function '__import_cse' hasn't been implemented, exiting")
            exit(1)

    def __import_eec_zipped(self) -> None:
        LOGGER.error(f"Function '__import_eec_zipped' hasn't been implemented, exiting")
        exit(1)

    def __import_eec(self) -> None:

        if self._library_extension == "zip":
            self.__import_eec_zipped()
        else:
            LOGGER.error(f"Function '__import_eec' hasn't been implemented, exiting")
            exit(1)

    def __import_snap_zipped(self) -> None:
        LOGGER.error(f"Function '__import_snap_zipped' hasn't been implemented, exiting")
        exit(1)

    def __import_snap(self) -> None:

        if self._library_extension == "zip":
            self.__import_snap_zipped()
        else:
            LOGGER.error(f"Function '__import_snap' hasn't been implemented, exiting")
            exit(1)
    
    def __postprocess_import(self) -> None:
        """
        1. Set the symbol's footprint to the library name
        2. Set the footprint's model to the library name
        """

        LOGGER.error(f"Function '__postprocess_import' hasn't been implemented, exiting")
        exit(1)


    def import_single(self) -> None:
        """
        """
        
        if self._source == SOURCE_CSE:
            self.__import_cse()

        elif self._source == SOURCE_EEC:
            self.__import_eec()

        elif self._source == SOURCE_SNAP:
            self.__import_snap()

        else:
            LOGGER.error(f"Unsupported source '{self._source}', exiting")
            exit(1)
        
        self.__postprocess_import()

    def import_multi(self) -> None:
        LOGGER.error(f"Function 'import_multi' hasn't been implemented, exiting")
        exit(1)