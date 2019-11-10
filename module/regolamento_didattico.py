# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def regolamentodidattico(update: Update, context: CallbackContext):
  update.message.reply_text(first_text(), reply_markup=regolamentodidattico_keyboard())

def regdid(update: Update, context: CallbackContext):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=first_text(), reply_markup=regolamentodidattico_keyboard())

def triennale(update: Update, context: CallbackContext):
  query = update.callback_query
  context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=imm_text(), reply_markup=triennale_keyboard())

def magistrale(update: Update, context: CallbackContext):
  query = update.callback_query
  context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=imm_text(), reply_markup=magistrale_keyboard())

def regolamenti(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    chat_id =update.effective_chat.id

    reg_doc = {
      'Regolamento Didattico 2019/2020': 'http://web.dmi.unict.it/sites/default/files/files/Regolamento%202019-20%20L%2031_Informatica.pdf',
      'Regolamento Didattico 2018/2019': 'http://web.dmi.unict.it/sites/default/files/files/L%2031%20Informatica(1).pdf',
      'Regolamento Didattico 2017/2018': 'http://web.dmi.unict.it/sites/default/files/files/Regolamento%20L%2031%20Informatica%202017-18.pdf',
      'Regolamento Didattico 2016/2017': 'http://web.dmi.unict.it/sites/default/files/files/Regolamento%20L%2031%20Informatica%202016-17.pdf',
      'Regolamento Didattico 2015/2016': 'http://web.dmi.unict.it/sites/default/files/files/Regolamento%20L%2031%20Informatica%202015-16.pdf',
      'Regolamento Didattico 2014/2015': 'http://web.dmi.unict.it/sites/default/files/files/Didattica%20Programmata%20e%20elenco%20propedeuticit%C3%A0%202014-2015.pdf',
      'Regolamento Didattico 2013/2014': 'http://web.dmi.unict.it/sites/default/files/files/regolamentoDidattico_L31_Informatica_1314.pdf',
      'Regolamento Didattico 2012/2013': 'http://web.dmi.unict.it/sites/default/files/files/regolamentoDidattico_L31_Informatica_1213.pdf',
      'Regolamento Didattico 2019/2020_m': 'http://web.dmi.unict.it/sites/default/files/Regolamento%20Didattico%20LM18%201920_0.pdf',
      'Regolamento Didattico 2018/2019_m': 'http://web.dmi.unict.it/sites/default/files/documenti_sito/Regolamento%20Didattico%20LM18%201819.pdf',
      'Regolamento Didattico 2017/2018_m': 'http://web.dmi.unict.it/sites/default/files/documenti_sito/Regolamento%20Didattico%20LM18%201718.pdf',
      'Regolamento Didattico 2016/2017_m': 'http://web.dmi.unict.it/sites/default/files/documenti_sito/LM%2018%20Informatica_1617.pdf',
      'Regolamento Didattico 2015/2016_m': 'http://web.dmi.unict.it/sites/default/files/documenti_sito/Regolamento%20Didattico%20LM18%201516.pdf'
    }

    context.bot.send_document(chat_id=chat_id, document=reg_doc[data])
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text="Ecco il file richiesto:",)
    
def regolamentodidattico_keyboard():
  keyboard = [
    [
      InlineKeyboardButton('Triennale', callback_data='reg_triennale_button'),
      InlineKeyboardButton('Magistrale', callback_data='reg_magistrale_button')]
    ]
  return InlineKeyboardMarkup(keyboard)

def triennale_keyboard():
  keyboard = [[InlineKeyboardButton('Regolamento Didattico 2019/2020', callback_data='Regolamento Didattico 2019/2020')],
              [InlineKeyboardButton('Regolamento Didattico 2018/2019', callback_data='Regolamento Didattico 2018/2019')],
              [InlineKeyboardButton('Regolamento Didattico 2017/2018', callback_data='Regolamento Didattico 2017/2018')],
              [InlineKeyboardButton('Regolamento Didattico 2016/2017', callback_data='Regolamento Didattico 2016/2017')],
              [InlineKeyboardButton('Regolamento Didattico 2015/2016', callback_data='Regolamento Didattico 2015/2016')],
              [InlineKeyboardButton('Regolamento Didattico 2014/2015', callback_data='Regolamento Didattico 2014/2015')],
              [InlineKeyboardButton('Regolamento Didattico 2013/2014', callback_data='Regolamento Didattico 2013/2014')],
              [InlineKeyboardButton('Regolamento Didattico 2012/2013', callback_data='Regolamento Didattico 2012/2013')],
              [InlineKeyboardButton('Indietro', callback_data='regdid_button')]]
  return InlineKeyboardMarkup(keyboard)

def magistrale_keyboard():
  keyboard = [[InlineKeyboardButton('Regolamento Didattico 2019/2020', callback_data='Regolamento Didattico 2019/2020_m')],
              [InlineKeyboardButton('Regolamento Didattico 2018/2019', callback_data='Regolamento Didattico 2018/2019_m,')],
              [InlineKeyboardButton('Regolamento Didattico 2017/2018', callback_data='Regolamento Didattico 2017/2018_m')],
              [InlineKeyboardButton('Regolamento Didattico 2016/2017', callback_data='Regolamento Didattico 2016/2017_m')],
              [InlineKeyboardButton('Regolamento Didattico 2015/2016', callback_data='Regolamento Didattico 2015/2016_m')],
              [InlineKeyboardButton('Indietro', callback_data='regdid_button')]]
  return InlineKeyboardMarkup(keyboard)

def first_text():
  return 'Scegliere uno dei seguenti corsi:'

def imm_text():
  return 'Scegliere il regolamento in base al proprio anno di immatricolazione:'
