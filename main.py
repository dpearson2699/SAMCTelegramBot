import constants as keys
import responses
import telegram
# import sheets
import os, sys
import pandas as pd
import gspread
import gspread_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import locale
from telegram.ext import *
from datetime import datetime

# bot = telegram.Bot(token=keys.API_KEY)
print("Bot started.")

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("tutorial").sheet1

# get data as a dataframe
data = gspread_dataframe.get_as_dataframe(sheet)
# data.Date = pd.to_datetime(data.Date)
# data.Data = data.Date.dt.strftime('%Y-%m')

# photoSent = False
# file_name = "image.jpg"
# image_tuple = (False, "image.jpg")


def start_command(update, context):
    update.message.reply_text('Type something to get started!')


def help_command(update, context):
    update.message.reply_text('Type a message and I\'ll echo it back.')


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = responses.sample_responses(text)
    update.message.reply_text(response)
#     update.message.reply_text(update.message.text) # in one line


def error(update, context):
    print("Update {update} caused error {context.error}")


def input_row(update, context):
    # entry = update.message.text
    # print("entry: " + entry)

    if update.message.photo:
        file = context.bot.getFile(update.message.photo[-1].file_id)
        print("file_id: " + str(update.message.photo[-1].file_id))
        # file.download('image.jpg')
        file_name = file.download()
        print(file_name)
        entry = file_name
        update.message.text = file_name

    # if update.message.text:
    else:
        entry = update.message.text

    print("entry: " + entry)

    user = update.message.from_user
    username = user['username']
    print(str(username))
    user_firstname = user['first_name']
    print(str(user_firstname))
    user_lastname = user['last_name']
    print(str(user_lastname))
    # datacheck = str(update.message.message_id) + '=' + str(
    #                                                     update.message.date) + '=' + 'category 1' + '=' + str(
    #                                                     entry) + '=' + str(username)
    datacheck = str(update.message.message_id) + '=' + 'category 1' + '=' + str(
        entry) + '=' + str(username)
    print("size: " + str(len(datacheck.encode('utf-8'))))  # max 64 bytes

    # entry = update.message.text.split(',')
    # try:
    #     entry[1] = float(entry[1])
    # except:
    #     # If this fails, the input text was not separated by a comma
    #     return

    # buttons displayed to the user showing categories
    buttons = [[]]
    buttons.append([])
    buttons.append([])
    # original:
    # buttons[0].append(telegram.InlineKeyboardButton(text='cat1',
    #                                                 callback_data=str(update.message.message_id) + '=' + str(
    #                                                     update.message.date) + '=' + 'category 1' + '=' + str(
    #                                                     entry)))
    # testing more columns:
    buttons[0].append(telegram.InlineKeyboardButton(text='Vehicle Photo',
                                                    callback_data=str(update.message.message_id) + '=' + 'Vehicle Photo' + '=' + str(
                                                        entry) + '=' + str(username)))

    buttons[0].append(telegram.InlineKeyboardButton(text='Mileage',
                                                    callback_data=str(update.message.message_id) + '=' + 'Mileage' + '=' + str(
                                                        entry) + '=' + str(username)))
    buttons[0].append(telegram.InlineKeyboardButton(text='Refueling',
                                                    callback_data=str(update.message.message_id) + '=' + 'Refueling' + '=' + str(
                                                        entry) + '=' + str(username)))
    buttons[1].append(telegram.InlineKeyboardButton(text='Equipment',
                                                    callback_data=str(
                                                        update.message.message_id) + '=' + 'Equipment' + '=' + str(
                                                        entry) + '=' + str(username)))
    buttons[2].append(telegram.InlineKeyboardButton(text='Report a problem',
                                                    callback_data=str(update.message.message_id) + '=' + 'Problem' + '=' + str(
                                                        entry) + '=' + str(username)))
    buttons[2].append(telegram.InlineKeyboardButton(text='Other',
                                                    callback_data=str(update.message.message_id) + '=' + 'Other' + '=' + str(
                                                        entry) + '=' + str(username)))

    # buttons[1].append(telegram.InlineKeyboardButton(text='cat6',
    #                                                 callback_data=str(update.message.message_id) + '=' + 'category 6' + '=' + str(
    #                                                     entry) + '=' + str(username)))
    # buttons[2].append(telegram.InlineKeyboardButton(text='cat7',
    #                                                 callback_data=str(update.message.message_id) + '=' + 'category 7' + '=' + str(
    #                                                     entry) + '=' + str(username)))
    # buttons[2].append(telegram.InlineKeyboardButton(text='cat8',
    #                                                 callback_data=str(update.message.message_id) + '=' + 'category 8' + '=' + str(
    #                                                     entry) + '=' + str(username)))
    # buttons[2].append(telegram.InlineKeyboardButton(text='cat9',
    #                                                 callback_data=str(update.message.message_id) + '=' + 'category 9' + '=' + str(
    #                                                     entry) + '=' + str(username)))

    # create a keyboard with the buttons
    keyboard = telegram.InlineKeyboardMarkup(buttons)
    # send the keyboard to the channel
    context.bot.send_message(update.message.chat_id, update.message.text, reply_markup=keyboard)


# def image_handler(update, context):  # saves photos sent to the bot in the working directory
#     file = bot.getFile(update.message.photo[-1].file_id)
#     print("file_id: " + str(update.message.photo[-1].file_id))
#     # file.download('image.jpg')
#     file_name = file.download()
#     print(file_name)
#     update.message.text = file_name
#     #Find a way to pass (True, file_name) to input_row


def callback_query_handler(update, context):
    try:
        # Once the user chooses a Type, we can go ahead and delete the keyboard to reduce clutter in the channel:
        context.bot.delete_message(update.callback_query.message.chat_id, str(update.callback_query.message.message_id))

        # Refresh connection with Google Sheets and data, in case there was any manual updates, so we avoid overwriting:
        client = gspread.authorize(creds)
        sheet = client.open('tutorial').sheet1
        data = sheet.get_all_records()

        # locale.setlocale(locale.LC_TIME, 'en_US.utf8')
        # date = str(datetime.strptime(update.callback_query.data.split('=')[1].split('+')[0], '%Y-%m-%d %H:%M:%S').strftime('%d/%b/%Y'))
        # date = str(datetime.datetime.now())
        now = datetime.now()
        date = now.strftime("%d/%m/%Y %H:%M:%S") #dd/mm/YY H:M:S
        print("date and time: " + date)
        category = update.callback_query.data.split('=')[1]
        description = update.callback_query.data.split('=')[2]
        username = update.callback_query.data.split('=')[3]

        row_to_insert = [date, category, description, username]
        sheet.insert_row(row_to_insert, len(data) + 2)  # To the amount of data rows, add 1 for the header, and write 1 below
        context.bot.send_message(update.callback_query.message.chat_id, 'Saved: ' + category + ' - ' + description)
    except:
        print("sorry :(")
        return


def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    # dp.add_handler(CommandHandler("start", start_command))
    # dp.add_handler(CommandHandler("help", help_command))
    # dp.add_handler(MessageHandler(Filters.text, handle_message))  # any message that's not a command
    # dp.add_error_handler(error)

    # dp.add_handler(MessageHandler(Filters.all, input_row))
    dp.add_handler(MessageHandler(Filters.all, input_row))
    # dp.add_handler(MessageHandler(Filters.photo, image_handler))
    dp.add_handler(CallbackQueryHandler(callback_query_handler))

    updater.start_polling()
    updater.idle()

main()

