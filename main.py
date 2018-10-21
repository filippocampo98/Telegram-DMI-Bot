# -*- coding: utf-8 -*-
from functions import *

bot = telegram.Bot(TOKEN)

with open('config/settings.yaml') as yaml_config:
	config_map = yaml.load(yaml_config)

def logging_message(bot, update):
	message_id = update.message.message_id #ID MESSAGGIO
	user = update.message.from_user # Restituisce un oggetto Telegram.User
	chat = update.message.chat # Restituisce un oggetto Telegram.Chat
	text = update.message.text #Restituisce il testo del messaggio
	date = update.message.date #Restituisce la data dell'invio del messaggio
	message = "\n___ID MESSAGE: " 	+ str(message_id) + "____\n" + \
			  "___INFO USER___\n" + \
			  "user_id:" 			+ str(user.id) + "\n" + \
			  "user_name:" 			+ str(user.username) + "\n" + \
			  "user_firstlastname:" + str(user.first_name) + " " + str(user.last_name) + "\n" + \
			  "___INFO CHAT___\n" + \
			  "chat_id:" 			+ str(chat.id) + "\n" + \
			  "chat_type:" 			+ str(chat.type)+"\n" + "chat_title:" + str(chat.title) + "\n" + \
			  "___TESTO___\n" + \
			  "text:" 				+ str(text) + \
			  "date:" 				+ str(date) + \
			  "\n_____________\n"

	log_tmp = open("logs/logs.txt","a+")
	log_tmp.write("\n"+message)


def main():
	updater = Updater(TOKEN, request_kwargs={'read_timeout': 20, 'connect_timeout': 20})
	dp = updater.dispatcher
	dp.add_handler(MessageHandler(Filters.all, logging_message),1)
	dp.add_handler(CallbackQueryHandler(button_handler))

	#Easter Egg
	dp.add_handler(CommandHandler('smonta_portoni',smonta_portoni))
	dp.add_handler(CommandHandler('santino',santino))
	dp.add_handler(CommandHandler('prof_sticker' ,prof_sticker))
	dp.add_handler(RegexHandler('/lezioni cazzeggio',bladrim))
	dp.add_handler(CommandHandler('leiCheNePensaSignorina',lei_che_ne_pensa_signorina))
	# dp.add_handler(RegexHandler('/forum',forum_bot))

	#Informative command
	dp.add_handler(CommandHandler('sdidattica', lambda bot, update: informative_callback(bot, update, 'sdidattica')))
	dp.add_handler(CommandHandler('sstudenti', lambda bot, update: informative_callback(bot, update, 'sstudenti')))
	dp.add_handler(CommandHandler('cea', lambda bot, update: informative_callback(bot, update, 'cea')))
	dp.add_handler(CommandHandler('ersu', lambda bot, update: informative_callback(bot, update, 'ersu')))
	dp.add_handler(CommandHandler('ufficioersu', lambda bot, update: informative_callback(bot, update, 'ufficioersu')))
	dp.add_handler(CommandHandler('urp', lambda bot, update: informative_callback(bot, update, 'urp')))
	dp.add_handler(CommandHandler('biblioteca', lambda bot, update: informative_callback(bot, update, 'biblioteca')))
	dp.add_handler(CommandHandler('cus', lambda bot, update: informative_callback(bot, update, 'cus')))

	dp.add_handler(CommandHandler('mensa', mensa_cmd))
	dp.add_handler(CommandHandler('mensa_plus', mensa_plus_cmd))

	dp.add_handler(CommandHandler('lezioni', lambda bot, update, args: lezioni(bot, update, args), pass_args=True))
	dp.add_handler(CommandHandler('esami', lambda bot, update, args: esami(bot, update, args), pass_args=True))

	dp.add_handler(CommandHandler('prof', prof, pass_args=True))

	dp.add_handler(CommandHandler('aulario', lambda bot, update: informative_callback(bot, update, 'aulario')))
	dp.add_handler(CommandHandler('help',help))
	dp.add_handler(CommandHandler('contributors', lambda bot, update: informative_callback(bot, update, 'contributors')))

	dp.add_handler(CommandHandler('rappresentanti', lambda bot, update: informative_callback(bot, update, 'rappresentanti')))
	dp.add_handler(CommandHandler('rappresentanti_dmi', lambda bot, update: informative_callback(bot, update, 'rappresentanti_dmi')))
	dp.add_handler(CommandHandler('rappresentanti_informatica', lambda bot, update: informative_callback(bot, update, 'rappresentanti_informatica')))
	dp.add_handler(CommandHandler('rappresentanti_matematica', lambda bot, update: informative_callback(bot, update, 'rappresentanti_matematica')))
	dp.add_handler(CommandHandler('chatid',give_chat_id))
	dp.add_handler(CommandHandler('send_log', send_log))
	dp.add_handler(CommandHandler('send_chat_ids', send_chat_ids))
	dp.add_handler(CommandHandler('errors', send_errors))
	dp.add_handler(CommandHandler('start', start))
	dp.add_handler(CommandHandler('avviso', newscommand))

	#JobQueue
	j = updater.job_queue

	j.run_repeating(avviso, interval=60) 											# job_dmi_news
	j.run_repeating(updater_lep, interval=86400, first=0) 							# job_updater_lep (24h)
	j.run_repeating(scrap, interval=3600, first=0) 									# job_mensa
	j.run_daily(mensa_notify_lunch, datetime.time(11, 45, 00), name='At 11:45') 	# job_mensa_lunch
	j.run_daily(mensa_notify_dinner, datetime.time(18, 45, 00), name='At 18:45') 	# job_mensa_dinner

	if (config_map['debug']['disable_drive'] == 0):
		dp.add_handler(CommandHandler('drive',drive))

	if config_map['debug']['disable_gitlab'] == 0:
		dp.add_handler(CommandHandler('git', git))
		dp.add_handler(CommandHandler('gitlab', git))

	if	config_map['debug']['disable_drive'] == 0 or \
		config_map['debug']['disable_gitlab'] == 0:
			dp.add_handler(RegexHandler('/request', request))
			dp.add_handler(RegexHandler('/add_db', add_db))

	if (config_map['debug']['disable_db'] == 0):
		dp.add_handler(CommandHandler('stats',stats))
		dp.add_handler(CommandHandler('stats_tot',stats_tot))

	if (config_map['debug']['disable_chatid_logs'] == 0):
		dp.add_handler(RegexHandler('/news',news_))
		dp.add_handler(CommandHandler('spamnews',spamnews))
		dp.add_handler(CommandHandler('disablenews',disablenews))
		dp.add_handler(CommandHandler('enablenews',enablenews))

	dp.add_handler(CallbackQueryHandler(callback))

	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
    main()
