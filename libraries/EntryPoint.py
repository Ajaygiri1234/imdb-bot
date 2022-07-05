from robot.libraries.BuiltIn import BuiltIn

from libraries.Communicate import RunItem
from libraries.Constants import COMPLETED, ERROR
from libraries.SetupError import setup_error
from Utils import log_to_console


def main():
    try:
        logger = BuiltIn().get_library_instance("BotLogger")
        log_to_console("Executing EntryPoint")

    except Exception as e:
        logger.logger.exception(f"{e}")
        setup_error(e, "main entry point error")
