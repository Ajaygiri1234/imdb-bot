from operator import index
from robot.libraries.BuiltIn import BuiltIn

from libraries.Communicate import RunItem
from libraries.Constants import COMPLETED, ERROR
from libraries.SetupError import setup_error
from Utils import log_to_console as print
from Utils import log_to_console
from imdbbot import Excel, Imdbbot
import pandas as pd


def main():
    try:
        # movie_list=['Halloween','The Matrix','Wrong movie','The Night Train to Kathmandu','The Shawshank Redemption','Titanic']
        excel=Excel()
        


        movie_list=excel.readmovies()
        bot=Imdbbot()
        result=bot.get_details(movie_list)
        excel.save_result(result)



        #logger = BuiltIn().get_library_instance("BotLogger")
        log_to_console("Executing EntryPoint")

    except Exception as e:
        #logger.logger.exception(f"{e}")
        setup_error(e, "main entry point error")
