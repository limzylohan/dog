import scrape
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from telegram import InlineKeyboardMarkup,InlineKeyboardButton 
#webscrape recent stories from straitstimes
stories = scrape.straits()



#create updater object
updater = Updater(token='686925777:AAErlg4bUJcx61IurDh6-DvHNJNKDmYdwb8')
#create a dispatcher object
dispatcher = updater.dispatcher

def start(straits_times_bot, update):
    straits_times_bot.send_message(chat_id=update.message.chat_id, text="Ello I'm the Straits Times bot, bringing you a summary of 5 of the latest news stories. Type /news to begin")

def commands(straits_times_bot, update):
    straits_times_bot.send_message(chat_id=update.message.chat_id, text="I can do the following functions \n /start short description\n /news brings the latest news")
    
def choose(bot, update):
    keyboard = []
    for i in range(5):
        keyboard.append([InlineKeyboardButton(stories[0][i], callback_data = 'story%s' %i)])

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def load_news(bot, update):
    query = update.callback_query
    summarized_news = ''


    if query['data'] == 'story0':
        summarized_news = scrape.return_url(stories,0)

    elif query['data'] == 'story1':
        summarized_news = scrape.return_url(stories,1)
    
    elif query['data'] == 'story2':
        summarized_news = scrape.return_url(stories,2)
    
    elif query['data'] == 'story3':
        summarized_news = scrape.return_url(stories,3)
    
    elif query['data'] == 'story4':
        summarized_news = scrape.return_url(stories,4)
    

    bot.edit_message_text(text=summarized_news,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)





updater.dispatcher.add_handler(CommandHandler('news', choose))
updater.dispatcher.add_handler(CallbackQueryHandler(load_news))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', commands))



updater.start_polling()
updater.idle()



