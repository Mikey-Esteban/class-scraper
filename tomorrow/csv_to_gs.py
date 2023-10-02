import gspread
import csv
from helpers import *

gc = gspread.oauth()

spreadsheetId_all = '1HEVy5YVR6hVyK7UuiiEIL_luQYNG2kAcBrpZHA5EuDA'  # Please set spreadsheet ID.
sheetName = 'All'  # Please set sheet name you want to put the CSV data.
csvFile = f'csv/{get_date()}/styles/all.csv'  # Please set the filename and path of csv file.

sh = gc.open_by_key(spreadsheetId_all)

sh.values_clear(sheetName)

sh.values_update(
    sheetName,
    params={'valueInputOption': 'USER_ENTERED'},
    body={'values': list(csv.reader(open(csvFile)))}
)

spreadsheetId_tabbed = '1etM9aRp0MDspxHVqQQ7u-TJCmi9HvruoZXX0QGG_6jg'  # Please set spreadsheet ID.
sheetName = 'Street_Data'  # Please set sheet name you want to put the CSV data.
csvFile = f'csv/{get_date()}/styles/street_styles_choreography.csv'  # Please set the filename and path of csv file.

sh = gc.open_by_key(spreadsheetId_tabbed)

sh.values_clear(sheetName)

sh.values_update(
    sheetName,
    params={'valueInputOption': 'USER_ENTERED'},
    body={'values': list(csv.reader(open(csvFile)))}
)

sheetName = 'Contemp_Data'  # Please set sheet name you want to put the CSV data.
csvFile = f'csv/{get_date()}/styles/contemporary_modern.csv'  # Please set the filename and path of csv file.

sh = gc.open_by_key(spreadsheetId_tabbed)

sh.values_clear(sheetName)

sh.values_update(
    sheetName,
    params={'valueInputOption': 'USER_ENTERED'},
    body={'values': list(csv.reader(open(csvFile)))}
)

sheetName = 'Jazz_Data'  # Please set sheet name you want to put the CSV data.
csvFile = f'csv/{get_date()}/styles/jazz.csv'  # Please set the filename and path of csv file.

sh = gc.open_by_key(spreadsheetId_tabbed)

sh.values_clear(sheetName)

sh.values_update(
    sheetName,
    params={'valueInputOption': 'USER_ENTERED'},
    body={'values': list(csv.reader(open(csvFile)))}
)

sheetName = 'Theater_Data'  # Please set sheet name you want to put the CSV data.
csvFile = f'csv/{get_date()}/styles/theater.csv'  # Please set the filename and path of csv file.

sh = gc.open_by_key(spreadsheetId_tabbed)

sh.values_clear(sheetName)

sh.values_update(
    sheetName,
    params={'valueInputOption': 'USER_ENTERED'},
    body={'values': list(csv.reader(open(csvFile)))}
)

sheetName = 'Ballet_Data'  # Please set sheet name you want to put the CSV data.
csvFile = f'csv/{get_date()}/styles/ballet.csv'  # Please set the filename and path of csv file.

sh = gc.open_by_key(spreadsheetId_tabbed)

sh.values_clear(sheetName)

sh.values_update(
    sheetName,
    params={'valueInputOption': 'USER_ENTERED'},
    body={'values': list(csv.reader(open(csvFile)))}
)

sheetName = 'Tap_Data'  # Please set sheet name you want to put the CSV data.
csvFile = f'csv/{get_date()}/styles/tap.csv'  # Please set the filename and path of csv file.

sh = gc.open_by_key(spreadsheetId_tabbed)

sh.values_clear(sheetName)

sh.values_update(
    sheetName,
    params={'valueInputOption': 'USER_ENTERED'},
    body={'values': list(csv.reader(open(csvFile)))}
)

sheetName = 'World_Data'  # Please set sheet name you want to put the CSV data.
csvFile = f'csv/{get_date()}/styles/world.csv'  # Please set the filename and path of csv file.

sh = gc.open_by_key(spreadsheetId_tabbed)

sh.values_clear(sheetName)

sh.values_update(
    sheetName,
    params={'valueInputOption': 'USER_ENTERED'},
    body={'values': list(csv.reader(open(csvFile)))}
)

sheetName = 'Other_Data'  # Please set sheet name you want to put the CSV data.
csvFile = f'csv/{get_date()}/styles/additional_disciplines.csv'  # Please set the filename and path of csv file.

sh = gc.open_by_key(spreadsheetId_tabbed)

sh.values_clear(sheetName)

sh.values_update(
    sheetName,
    params={'valueInputOption': 'USER_ENTERED'},
    body={'values': list(csv.reader(open(csvFile)))}
)

# sh = gc.open("CA Daily Dance Schedule")
# print(sh.sheet1.get('A1'))