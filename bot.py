import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from config import TOKEN
from options import options
import requests

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def error(bot, update):
    logger.error("Update '%s' has caused '%s'", update, update.error)


def support(update, context, *args):
    author = update.message.from_user.first_name
    message = """Welcome, {}! 
I'm BuyUCoin Ticket Bot. Kindly select the below mentioned options to move forward. 
    """.format(
        author
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Support Email", url="https://www.buyucoin.com/contact"
                    ),
                    InlineKeyboardButton(
                        text="Support Ticket",
                        url="https://buyucoin.freshdesk.com/support/tickets/new",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="0% Fees Trading",
                        url="https://trade.buyucoin.com/direct-buy-sell-bitcoin?market=btc-inr",
                    ),
                    InlineKeyboardButton(
                        text="Market Trading",
                        url="https://trade.buyucoin.com/markets",
                    ),
                ],
            ]
        ),
    )


def start(update, context, *args):
    print(update)
    author = update.message.from_user.first_name
    emoji = u"\U0001F604"
    message = """Hi, {}! 
I'm BuyUCoin Ticket Bot. Press / to get started {}. 
    """.format(
        author, emoji
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("support", support))
    # dp.add_handler(CommandHandler("help", _help))
    # dp.add_handler(MessageHandler(Filters.text, echo_text))
    dp.add_error_handler(error)
    # for i in options.keys():
    #     j = "{}@buyucointickerbot".format(i)
    #     dp.add_handler(
    #         CommandHandler([i, j], lambda update, context: universal(update, context))
    #     )
    dp.add_handler(
        CommandHandler(options, lambda update, context: universal(update, context))
    )
    # dp.add_handler(
    #     CommandHandler(
    #         ["{}@buyucointickerbot".format(i) for i in options.keys()],
    #         lambda update, context: universal(update, context),
    #     )
    # )
    updater.start_polling()
    logger.info("Started polling.........")
    updater.idle()


def universal(update, context, *args):
    print(*args)
    name = update.message["text"][1:]
    if "@" in name:
        name = name.split("@")[0]
    url = "https://api.buyucoin.com/market/v1.0/getLiveOtcMarketData"
    data = requests.post(url).json()["data"][options[name]]
    message = r"""<pre>
Market                  | {}
Market Cap rank         | {}


Sell Price              | {}
Buy Price               | {}
Min Sell Trade          | {}
Min Buy Trade           | {}
24Hr change             | {}
24Hr change percent     | {}%
</pre>
""".format(
        data["name"],
        data['marketCapRank'],
        data['INR']['sellPrice'],
        data['INR']['buyPrice'],
        data['INR']['minSellTrade'],
        data['INR']['minBuyTrade'],
        data['INR']['c24'],
        data['INR']['c24p']
   )
    #message = str(data['name'])
    context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=message,
    parse_mode=ParseMode.HTML,
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Trade at 0% ", url="https://trade.buyucoin.com"
                    ),
                    InlineKeyboardButton(
                        text="OTC Desk",
                        url="https://trade.buyucoin.com/direct-buy-sell-bitcoin?market=btc-inr",
                    ),
                ]
            ]
        ),
    )


# update

if __name__ == "__main__":
    main()