import telegram, logging

import modules.dmibot.managers.markdown_manager as markdown_manager

# Markdown messages handler
# Responsible for loading markdown texts and send them as messages when requested
def menu_cmd_callback_handler(update, context):
    bot = context.bot

    query = update.callback_query
    query_data = query.data.split(",")
    user_id = query.from_user.id

    username = query.message.chat.username
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    logging.info("Handling menu_cmd callback data from {}: {}".format(chat_id, query_data))

    action = query_data[1]

    if action == "exit":
        bot.delete_message(
            chat_id = chat_id,
            message_id = message_id
        )