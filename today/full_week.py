import datetime
from datetime import date
from selenium.webdriver.common.by import By
from helpers import *

def run_full_week_csv(browser, tab_id, studio_name, date_format):

    next_day = date.today()

    move_to_table(browser, tab_id)

    browser.implicitly_wait(.3)
    flag, counter = False, 0
    all_rows = browser.find_element(By.ID, "classSchedule-mainTable").find_elements(By.TAG_NAME, 'tr')
    correct_date_rows = []

    for row in all_rows:
        if counter > 0 and flag == False: continue
        try: 
            date_formatted = datetime.datetime.strptime(row.text.strip(), date_format).date()
            if next_day == date_formatted:
                flag, counter = True, 1
            else:
                flag = False
        except:
            if flag:
                correct_date_rows.append(row)

    class_data = get_class_data(browser, correct_date_rows, studio_name)

    return class_data