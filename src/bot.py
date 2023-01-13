"""Bot module"""

from os import getenv, path
import logging
from logging import config

import requests
from telegram.ext import Updater, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from dotenv import load_dotenv      # load variables from local environment
load_dotenv()

BOT_API = "5231238723:AAFppyPBD3VKzj_-kHMXquwEVv1fAcOJCl4" # Your bot api
OMDB = "https://math24.aparsclassroom.com/api/live/today"
OMDB_API = getenv("OMDB_API")   # Your omdb api
IMDB_TRAILER_REQ = "https://imdb-api.com/en/API/YouTubeTrailer"
IMDB_API = getenv("IMDB_API")   # Your imdb api
IMDB_LINK = "https://www.imdb.com/title/"


class Bot:
    """Bot operations

    Available bot commands and operations
    API requests
    """
    HELP_MSG = "Available commands:\n" \
               "    /help\n" \
               "    /find [title] [y=year] (/find The Godfather y=1972)\n" \
               "After you find a movie, use buttons under it to get more information or " \
               "use commands to get information about last movie from bot memory:\n" \
               "    /rate|/rated -- movie PG\n" \
               "    /award|/awards -- awards and nominations\n" \
               "    /rating|/ratings -- movie ratings\n" \
               "    /language|/languages -- movie languages\n" \
               "    /plot -- short plot description\n" \
               "    /link - IMDB movie page\n"

    def __init__(self) -> None:
        """Initialize bot and his logger"""
        # Set up bot updater and dispatcher
        self.updater = Updater(BOT_API, use_context=True)
        self.dp = self.updater.dispatcher
        # Set up logger with bot config
        logging.config.fileConfig(path.join(path.dirname(path.abspath(__file__)), 'logging.conf'))
        self.logger = logging.getLogger(__name__)  # Create logger
        # Set up bot memory
        self.memory: dict = {}  # last title that user found, stored in memory

    def start(self, update: Update, context: CallbackContext) -> None:
        """Message that prints for new users"""
        self.logger.info("/start called")
        update.message.reply_text("Hello, I'm MovieBot :) -> /help")

    def help_text(self, update: Update, context: CallbackContext) -> None:
        """/help message"""
        self.logger.info("/help called")
        update.message.reply_text(self.HELP_MSG)

    def any_text(self, update: Update, context: CallbackContext) -> None:
        """Bot response on not coded text"""
        self.logger.info(f"unknown command called ({update.message.text})")
        update.message.reply_text(f"Unknown command: {update.message.text} -> /help")

    def error(self, update: Update, context: CallbackContext) -> None:
        """Logs errors"""
        self.logger.exception(f"error: {context.error} - "
                              f"['{update['message']['chat']['first_name']}': '{update['message']['text']}']")
        update.message.reply_text("Sorry, this movie/show is unknown to me")

    @staticmethod
    def empty_memory(update: Update):
        update.message.reply_text("My memory is empty😕.\nLook something up! -> /find")

    def find_title(self, update: Update, context: CallbackContext) -> None:
        """/find command

        Finds movie by specifications
        """
        self.logger.info("/find called")
        if "y=" in context.args[-1]:                    # check arguments for year specification
            movie_name = " ".join(context.args[:-1])
            omdb_params = {
                
                "ajk": movie_name,
                "y": context.args[-1][2:]
            }
        else:
            movie_name = " ".join(context.args)
            omdb_params = {
                
                "ajk": movie_name,
            }
        response = requests.get(OMDB, params=omdb_params)
        movie_data = self.memory = response.json()                                  # Save found title in memory
        data_str = f"🗂️ Course::    {movie_data['Batch']} ({movie_data['Paper']})\n" \
                   f"Genre:    {movie_data['Video_Description']}\n" \


        poster = requests.get(movie_data["thumbnail_path"]).content
        context.bot.sendMediaGroup(chat_id=update.effective_chat.id,
                                   media=[InputMediaPhoto(poster)])  # Show poster

        buttons = [[InlineKeyboardButton("Plot", callback_data=f"{movie_data['thumbnail_path']}:plot"),
                   InlineKeyboardButton("Trailer", url=self.get_trailer_url(movie_data["thumbnail_path"])),
                   
        update.message.reply_text(data_str, reply_markup=InlineKeyboardMarkup(buttons))

    
