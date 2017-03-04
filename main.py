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
	dp.add_handler(CallbackQueryHandler(button_handler))

	dp.add_handler(RegexHandler('/help',help))
	dp.add_handler(RegexHandler('/rappresentanti',rappresentanti))
	dp.add_handler(RegexHandler('/rappresentanti_dmi',rappresentanti_dmi))
	dp.add_handler(RegexHandler('/rappresentanti_informatica',rappresentanti_info))
	dp.add_handler(RegexHandler('/rappresentanti_matematica',rappresentanti_mate))
	dp.add_handler(RegexHandler('/sdidattica',sdidattica))
	dp.add_handler(RegexHandler('/sstudenti',sstudenti))
	dp.add_handler(RegexHandler('/cea',cea))
	dp.add_handler(RegexHandler('/ersu',ersu))
	dp.add_handler(RegexHandler('/ufficioersu',ufficioersu))
	dp.add_handler(RegexHandler('/urp',urp))
	dp.add_handler(RegexHandler('/prof',prof))
	dp.add_handler(RegexHandler('/esami',esami))
	dp.add_handler(RegexHandler('/mesami',mesami))
	dp.add_handler(CommandHandler('aulario',aulario))
	dp.add_handler(CommandHandler('mensa',mensa))
	dp.add_handler(CommandHandler('biblioteca',biblioteca))
	dp.add_handler(CommandHandler('cus',cus))
	dp.add_handler(CommandHandler('smonta_portoni',smonta_portoni))
	dp.add_handler(CommandHandler('santino',santino))
	dp.add_handler(CommandHandler('liste',liste))
	dp.add_handler(CommandHandler('contributors',contributors))
	dp.add_handler(RegexHandler('/forum',forum_bot))

	if (disable_drive == 0):
	  dp.add_handler(CommandHandler('drive',drive))
	  dp.add_handler(RegexHandler('/adddb',adddb))
	  dp.add_handler(RegexHandler('/request',request))

	if (disable_db == 0):
	  dp.add_handler(CommandHandler('stats',stats))
	  dp.add_handler(CommandHandler('stats_tot',statsTot))

	if (disable_chatid_logs == 0):
	  dp.add_handler(RegexHandler('/news',news_))
	  dp.add_handler(CommandHandler('spamnews',spamnews))
	  dp.add_handler(CommandHandler('disablenews',disablenews))
	  dp.add_handler(CommandHandler('enablenews',enablenews))


	dp.add_handler(CallbackQueryHandler(callback))

	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
    main()
