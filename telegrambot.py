# -*- coding: utf-8 -*-
from utilities import *

reload(sys)
sys.setdefaultencoding('utf8')

bot= telegram.Bot(TOKEN)
updater = Updater(TOKEN)
# Get the dispatcher to register handlers
dp = updater.dispatcher

def main():
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
	dp.add_handler(RegexHandler('/aulario',aulario))
	dp.add_handler(RegexHandler('/mensa',mensa))
	dp.add_handler(RegexHandler('/biblioteca',biblioteca))
	dp.add_handler(RegexHandler('/cus',cus))
	dp.add_handler(RegexHandler('/smonta_portoni',smonta_portoni))
	dp.add_handler(RegexHandler('/santino',santino))
	dp.add_handler(RegexHandler('/liste',liste))
	dp.add_handler(RegexHandler('/contributors',contributors))
	dp.add_handler(RegexHandler('/forum',forum_bot))

	if (disable_drive == 0):
	  dp.add_handler(RegexHandler('/drive',drive))
	  dp.add_handler(RegexHandler('/adddb',adddb))
	  dp.add_handler(RegexHandler('/request',request))

	if (disable_db == 0):
	  dp.add_handler(RegexHandler('/stats',stats))
	  dp.add_handler(RegexHandler('/statsT',statsTot))

	if (disable_logs == 0):
	  dp.add_handler(RegexHandler('/news',news_))
	  dp.add_handler(RegexHandler('/spamnews',spamnews))
	  dp.add_handler(RegexHandler('/disablenews',disablenews))
	  dp.add_handler(RegexHandler('/enablenews',enablenews))


	dp.add_handler(CallbackQueryHandler(callback))

	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
    main()
