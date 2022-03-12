#!/usr/bin/env python3

"""Telegram movie/show information bot
By using omdb & imdb APIs
"""

__author__ = "Aleksandr Verevkin"
__license__ = "GNU GPL v.3"
__maintainer__ = "Aleksandr Verevkin"
__status__ = "Production"

from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from bot import Bot
# TODO separate print method
# TODO buttons memory
# TODO IMDB link
# TODO trailer


def main():
    bot = Bot()  # Bot initialization
    bot.logger.info("Bot is initialized and maintained")

    bot.dp.add_handler(CommandHandler("start", bot.start))  # Commands
    bot.dp.add_handler(CommandHandler("help", bot.help_text))

    bot.dp.add_handler(CommandHandler("find", bot.find_title))  # Movie commands
    bot.dp.add_handler(CommandHandler("rate", bot.rated))
    bot.dp.add_handler(CommandHandler("rated", bot.rated))
    bot.dp.add_handler(CommandHandler("language", bot.language))
    bot.dp.add_handler(CommandHandler("award", bot.awards))
    bot.dp.add_handler(CommandHandler("awards", bot.awards))
    bot.dp.add_handler(CommandHandler("plot", bot.plot))
    bot.dp.add_handler(CommandHandler("rating", bot.rating))
    bot.dp.add_handler(CommandHandler("ratings", bot.rating))

    bot.dp.add_handler(MessageHandler(Filters.text, bot.any_text))  # Any other message

    bot.dp.add_handler(CallbackQueryHandler(bot.query_handler))

    bot.dp.add_error_handler(bot.error)  # Error

    bot.updater.start_polling()  # Start idling for messages
    bot.updater.idle()

    bot.logger.info("Bot terminated.")


if __name__ == "__main__":
    main()