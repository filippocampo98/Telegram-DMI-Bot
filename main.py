# -*- coding: utf-8 -*-
from functions import *

reload(sys)
sys.setdefaultencoding('utf8')

bot= telegram.Bot(TOKEN)

def record_everything(bot, update):
	message = str(update.message)
	log_tmp = open("logs/logs.txt","a+")
	log_tmp.write("\n"+message)

def main():
	updater = Updater(TOKEN)
	dp = updater.dispatcher
	dp.add_handler(MessageHandler(Filters.all, record_everything),1)
	dp.add_handler(RegexHandler('/help',help))

	dp.add_handler(CommandHandler('rappresentanti',rappresentanti))
	dp.add_handler(CommandHandler('rappresentanti_dmi',rappresentanti_dmi))
	dp.add_handler(CommandHandler('rappresentanti_informatica',rappresentanti_info))
	dp.add_handler(CommandHandler('rappresentanti_matematica',rappresentanti_mate))

	dp.add_handler(RegexHandler('/prof',prof))

	'''
	dp.add_handler(RegexHandler('/esami',esami))
	'''

	dp.add_handler(RegexHandler('/mesami',mesami))

	dp.add_handler(RegexHandler('/smonta_portoni',smonta_portoni))
	dp.add_handler(RegexHandler('/santino',santino))

	'''
	dp.add_handler(RegexHandler('/liste',liste))
	dp.add_handler(RegexHandler('/forum',forum_bot))
	'''

	dp.add_handler(CommandHandler('sdidattica', lambda bot, update: custom_callback(bot, update, 'sdidattica')))
	dp.add_handler(CommandHandler('sstudenti', lambda bot, update: custom_callback(bot, update, 'sstudenti')))
	dp.add_handler(CommandHandler('cea', lambda bot, update: custom_callback(bot, update, 'cea')))
	dp.add_handler(CommandHandler('ersu', lambda bot, update: custom_callback(bot, update, 'ersu')))
	dp.add_handler(CommandHandler('ufficioersu', lambda bot, update: custom_callback(bot, update, 'ufficioersu')))
	dp.add_handler(CommandHandler('urp', lambda bot, update: custom_callback(bot, update, 'urp')))
	dp.add_handler(CommandHandler('mensa', lambda bot, update: custom_callback(bot, update, 'mensa')))
	dp.add_handler(CommandHandler('biblioteca', lambda bot, update: custom_callback(bot, update, 'biblioteca')))
	dp.add_handler(CommandHandler('cus', lambda bot, update: custom_callback(bot, update, 'cus')))
	dp.add_handler(CommandHandler('contributors', lambda bot, update: custom_callback(bot, update, 'contributors')))

	dp.add_handler(CommandHandler('lezioni', lezioni, pass_args=True))
	dp.add_handler(CommandHandler('aulario', aulario))

	if (disable_drive == 0):
	  dp.add_handler(RegexHandler('/drive',drive))
	  dp.add_handler(RegexHandler('/adddb',adddb))
	  dp.add_handler(RegexHandler('/request',request))

	if (disable_db == 0):
	  dp.add_handler(RegexHandler('/stats',stats))
	  dp.add_handler(RegexHandler('/statsT',statsTot))

	if (disable_chatid_logs == 0):
	  dp.add_handler(RegexHandler('/news',news_))
	  dp.add_handler(RegexHandler('/spamnews',spamnews))
	  dp.add_handler(RegexHandler('/disablenews',disablenews))
	  dp.add_handler(RegexHandler('/enablenews',enablenews))


	dp.add_handler(CallbackQueryHandler(callback))

	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
    main()
