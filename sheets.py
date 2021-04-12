## From Tim
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# from pprint import pprint
import gspread_dataframe # from bookkeeping tutorial
import numpy as np
import pandas as pd

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("tutorial").sheet1

# data = sheet.get_all_records()
# pprint(data)
#
# row = sheet.row_values(2)
# pprint(row)
#
# col = sheet.col_values(2)
# pprint(col)
#
# cell = sheet.cell(1,2).value
# pprint(cell)

# insert row:
# insertRow = ["4/2/2021", "cat1", "hello again"]
# sheet.insert_row(insertRow, 2)  # doesn't replace the row, just pushes it down

# delete row: just need index
# sheet.delete_row(3)  # everything under that row will shift up

# update cell:
# sheet.update_cell(2, 3, "HELLO")

# numRows = sheet.row_count
# print(numRows)  # returns 1000
# print(len(data))  # doesn't count header


## From bookkeeping tutorial
data = gspread_dataframe.get_as_dataframe(sheet)
data.Date = pd.to_datetime(data.Date)

