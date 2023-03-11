import datetime
import pandas as pd
from selenium.webdriver.common.by import By
from datetime import date

from helpers import *

def runAtdf(browser):

    day = date.today() + datetime.timedelta(days=1)

    config = {
        'tabId': 'tabA118',
        'filename': 'atdf_inclass.csv',
        'day': day
    }

    move_to_table(browser, config)

    browser.implicitly_wait(.1)
    flag = False
    all_rows = browser.find_element(By.ID, "classSchedule-mainTable").find_elements(By.TAG_NAME, 'tr')
    correct_date_rows = []
    # class_data = [
    #     ['time', 'name', 'instructor']
    # ]

    for row in all_rows:
        try: 
            row.find_element(By.CLASS_NAME, 'header')
            date_formatted = datetime.datetime.strptime(row.text.strip(), '%a %B %d, %Y').date()
            if config['day'] == date_formatted:
                flag = True
            else:
                flag = False
        except:
            if flag:
                correct_date_rows.append(row)
    
    class_data = []

    header_row = browser.find_elements(By.CLASS_NAME, 'floatingHeader-loaded')
    header_data = []
    for th in header_row:
        header_data.append('Sign up') if th.text == ' ' else header_data.append(th.text)
    
    class_data.append(header_data)
    
    class_data = get_class_data(correct_date_rows, class_data)

    # for row in all_rows:
    #     try: 
    #         row.find_element(By.CLASS_NAME, 'header')
    #         date_formatted = datetime.datetime.strptime(row.text.strip(), '%a %B %d, %Y').date()
    #         if config['day'] == date_formatted:
    #             flag = True
    #         else:
    #             flag = False
    #     except:
    #         if flag:
    #             data = get_class_data(row)
    #             if data:
    #                 class_data.append(data)

    pd.DataFrame(class_data).to_csv(f"csv/{config['filename']}", header=False)