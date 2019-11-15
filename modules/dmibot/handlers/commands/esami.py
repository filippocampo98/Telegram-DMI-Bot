import telegram, logging, sqlite3

import modules.pytg.managers.text_manager as text_manager

from modules.dmibot.utils.sqlite3_utils import *

def esami_cmd_handler(update, context):
    bot = context.bot
    args = context.args

    message = update.message
    chat_id = message.chat.id

    username = message.from_user.username
    user_id = message.from_user.id

    logging.info("Received esami command update from {} ({}) in chat {}".format(username, user_id, chat_id))
    
    phrases = text_manager.load_phrases()

    # msg_text = "Inserisci un parametro valido\n"

    if not args:
        msg_text = "Inserisci almeno uno dei seguenti parametri: giorno, materia, sessione (prima, seconda, terza, straordinaria)."

        bot.send_message(
            chat_id = chat_id,
            text = msg_text
        )
        return 

    output = set()

    conn = sqlite3.connect('data/DMI_DB.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute("SELECT * FROM exams")
    items = cur.fetchall()
    conn.close()

    # Clear arguments - Trasform all to lower case - Remove word 'anno', 'sessione'
    args = [x.lower() for x in args if len(x) > 2]
    if 'anno' in args:
        args.remove('anno')

    if 'sessione' in args:
        args.remove('sessione')

    # Study case
    if len(args) == 1:
        if args[0] in ("primo", "secondo", "terzo"):
            output = esami_condition(items, "anno", args[0])

        elif args[0] in ("prima", "seconda", "terza", "straordinaria"):
            output = esami_condition(items, "sessione", args[0], True)

        elif [item["insegnamento"].lower().find(args[0]) for item in items]:
            output = esami_condition(items, "insegnamento", args[0])

    elif len(args) > 1:
        # Create an array of session and years if in arguments
        sessions = list(set(args).intersection(("prima", "seconda", "terza", "straordinaria")))
        years = list(set(args).intersection(("primo", "secondo", "terzo")))

        _years = {
            "primo": "1° anno",
            "secondo": "2° anno",
            "terzo": "3° anno"
        }
        for i in range(len(years)):
            years[i] = _years[years[i]]

        if sessions and years:
            for item in items:
                if (item["anno"] in years) and ([session for session in sessions if [appeal for appeal in item[session] if appeal]]):
                    output.add(esami_output(item, sessions))

        elif sessions and not years:
            # If years array is empty and session not, the other word are subjects
            subjects = [arg for arg in args if arg not in(sessions)]

            if subjects:
                for item in items:
                    for subject in subjects:
                        if [session for session in sessions if [appeal for appeal in item[session] if appeal]] and subject in item["insegnamento"].lower():
                            output.add(esami_output(item, sessions))

        elif not sessions and not years:
            for arg in args:
                output = output.union(esami_condition(items, "insegnamento", arg))

    output = split_esami_output(output)

    for block in output:
        bot.send_message(
            chat_id = chat_id,
            text = '\n'.join(list(block)),
            parse_mode = telegram.ParseMode.MARKDOWN
        )

def esami_condition(items, field, value, *session):
	output = set()

	if field == "anno":
		years = {
			"primo": "1° anno",
			"secondo": "2° anno",
			"terzo": "3° anno"
		}
		value = years[value]

	if session:
		for item in items:
			if ([appeal for appeal in item[value] if appeal]):
				output.add(esami_output(item, [value]))
	else:
		for item in items:
			if(value in item[field].lower()):
				output.add(esami_output(item, ("prima", "seconda", "terza", "straordinaria")))

	return output

def esami_output(item, sessions):

	output = "*Insegnamento:* " + item["insegnamento"]
	output += "\n*Docenti:* " + item["docenti"]

	for session in sessions:
		appeal = item[session]
		if appeal:
			appeal = str(appeal)
			appeal = appeal.replace("[", "")
			appeal = appeal.replace("]", "")
			appeal = appeal.replace("'", "")
			appeal = appeal.split("', '")
			if "".join(appeal) != "":
				output += "\n*" + session.title() + ":* " + " | ".join(appeal)

	output += "\n*CDL:* " + item["cdl"]
	output += "\n*Anno:* " + item["anno"] + "\n"

	return output

def esami_check_output(output):
	if len(output):
		output_str = '\n'.join(list(output))
		output_str += "\n Risultati trovati: " + str(len(output))
	else:
		output_str = "Nessun risultato trovato :(\n"

	return output_str

def split_esami_output(output):
    blocks = []

    buffer = []

    current_lines = 0
    max_lines = 10

    for line in output:
        buffer.append(line)

        current_lines += 1

        if current_lines >= max_lines:
            blocks.append(buffer)
            buffer = []
            current_lines = 0

    return blocks
