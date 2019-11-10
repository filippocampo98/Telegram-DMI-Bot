# -*- coding: utf-8 -*-
from functions import *
from module.shared import config_map

bot = telegram.Bot(config_map["token"])

def logging_message(update: Update, context: CallbackContext):
	try:
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
	except:
		pass


def main():
	updater = Updater(TOKEN, request_kwargs={'read_timeout': 20, 'connect_timeout': 20}, use_context=True)
	dp = updater.dispatcher
	dp.add_handler(MessageHandler(Filters.all, logging_message),1)

	#Easter Egg
	dp.add_handler(CommandHandler('smonta_portoni',smonta_portoni))
	dp.add_handler(CommandHandler('santino',santino))
	dp.add_handler(CommandHandler('prof_sticker' ,prof_sticker))
	dp.add_handler(MessageHandler(Filters.regex('/lezioni cazzeggio'), bladrim))
	dp.add_handler(CommandHandler('leiCheNePensaSignorina',lei_che_ne_pensa_signorina))

	#Informative command
	dp.add_handler(CommandHandler('sdidattica', lambda update, context: informative_callback(update, context, 'sdidattica')))
	dp.add_handler(CommandHandler('sstudenti', lambda update, context: informative_callback(update, context, 'sstudenti')))
	dp.add_handler(CommandHandler('cea', lambda update, context: informative_callback(update, context, 'cea')))
	dp.add_handler(CommandHandler('ersu', lambda update, context: informative_callback(update, context, 'ersu')))
	dp.add_handler(CommandHandler('ufficioersu', lambda update, context: informative_callback(update, context, 'ufficioersu')))
	dp.add_handler(CommandHandler('urp', lambda update, context: informative_callback(update, context, 'urp')))
	dp.add_handler(CommandHandler('biblioteca', lambda update, context: informative_callback(update, context, 'biblioteca')))
	dp.add_handler(CommandHandler('cus', lambda update, context: informative_callback(update, context, 'cus')))

	dp.add_handler(CommandHandler('lezioni', lambda update, context: lezioni(update, context)))
	dp.add_handler(CommandHandler('esami', lambda update, context: esami(update, context)))

	dp.add_handler(CommandHandler('prof', prof))

	dp.add_handler(CommandHandler('aulario', lambda update, context: informative_callback(update, context, 'aulario')))
	dp.add_handler(CommandHandler('help',help))
	dp.add_handler(CommandHandler('contributors', lambda update, context: informative_callback(update, context, 'contributors')))

	dp.add_handler(CommandHandler('rappresentanti', lambda update, context: informative_callback(update, context, 'rappresentanti')))
	dp.add_handler(CommandHandler('rappresentanti_dmi', lambda update, context: informative_callback(update, context, 'rappresentanti_dmi')))
	dp.add_handler(CommandHandler('rappresentanti_informatica', lambda update, context: informative_callback(update, context, 'rappresentanti_informatica')))
	dp.add_handler(CommandHandler('rappresentanti_matematica', lambda update, context: informative_callback(update, context, 'rappresentanti_matematica')))
	dp.add_handler(CommandHandler('report', report))
	dp.add_handler(CommandHandler('chatid',give_chat_id))
	dp.add_handler(CommandHandler('send_log', send_log))
	dp.add_handler(CommandHandler('send_chat_ids', send_chat_ids))
	dp.add_handler(CommandHandler('errors', send_errors))
	dp.add_handler(CommandHandler('start', start))
	dp.add_handler(CommandHandler('cloud', lambda update, context: informative_callback(update, context, 'cloud')))

  # generic buttons
	dp.add_handler(CallbackQueryHandler(generic_button_handler, pattern='^(esami_buttonlezioni_button|help_cmd|exit_cmd)'))
	dp.add_handler(CallbackQueryHandler(submenu_handler,        pattern='sm_*'))
	dp.add_handler(CallbackQueryHandler(md_handler,             pattern='md_*'))

  # drive & gitlab buttons
	dp.add_handler(CallbackQueryHandler(callback,               pattern='Drive_*'))
	dp.add_handler(CallbackQueryHandler(gitlab_handler,         pattern='git_*'))

	# regolamento didattico
	dp.add_handler(CommandHandler('regolamentodidattico', regolamentodidattico))
	dp.add_handler(CallbackQueryHandler(triennale,                   pattern='reg_triennale_button'))
	dp.add_handler(CallbackQueryHandler(magistrale,                  pattern='reg_magistrale_button'))
	dp.add_handler(CallbackQueryHandler(regdid,                      pattern='regdid_button'))
	dp.add_handler(CallbackQueryHandler(regolamenti,                 pattern='Regolamento*'))
	dp.add_handler(CallbackQueryHandler(regolamentodidattico_button, pattern='regolamentodidattico_button'))

	#JobQueue
	j = updater.job_queue

	j.run_repeating(updater_lep, interval=86400, first=0) 				# job_updater_lep (24h)

	if (config_map['debug']['disable_drive'] == 0):
		dp.add_handler(CommandHandler('drive',drive))

	if config_map['debug']['disable_gitlab'] == 0:
		dp.add_handler(CommandHandler('git', git))
		dp.add_handler(CommandHandler('gitlab', git))

	if	config_map['debug']['disable_drive'] == 0 or \
		config_map['debug']['disable_gitlab'] == 0:
			dp.add_handler(MessageHandler(Filters.regex('/request'), request))
			dp.add_handler(MessageHandler(Filters.regex('/add_db'), add_db))

	if (config_map['debug']['disable_db'] == 0):
		dp.add_handler(CommandHandler('stats',stats))
		dp.add_handler(CommandHandler('stats_tot',stats_tot))

	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
    main()
