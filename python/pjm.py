import os
import pandas as pd
from selenium import webdriver
from helpers import *
import datetime
import time

base_url = 'https://www.pjmstudionyc.com/'

def isManhattan(str):
    return str == '[MAN]'

def run():
    if not os.path.exists(f"csv/{get_date()}"):
        os.makedirs(f"csv/{get_date()}")

    next_day_formatted = (date.today() + datetime.timedelta(days=1)).strftime('%a %d')
    browser = webdriver.Firefox()
    browser.implicitly_wait(20)
    browser.get(base_url)
    
    print('running for studio...', 'pjm')
    dates_rows = browser.find_elements(By.CLASS_NAME, 'sZqbM3k')
    correct_date_index = -1

    for i, date_row in enumerate(dates_rows):
        reformatted_date = ' '.join(date_row.text.split('\n'))
        if reformatted_date == next_day_formatted: correct_date_index = i

    manhattan_classes = [['Time', 'Class', 'Instructor', 'Length']]
    lic_classes = [['Time', 'Class', 'Instructor', 'Length']]

    correct_date_container = dates_rows[correct_date_index]
    correct_date_row = correct_date_container.find_element(By.CLASS_NAME, 'sLoech5')
    classes_rows = correct_date_row.find_elements(By.CLASS_NAME, 'sYbjzkn')
    for class_row in classes_rows:

        class_data = class_row.text.split('\n')[:3]

        if isManhattan(class_data[1].split(' ')[0]):
            manhattan_classes.append(class_data)
        else:
            lic_classes.append(class_data)

    if len(manhattan_classes) > 1:
        pd.DataFrame(manhattan_classes).to_csv(f"csv/{get_date()}/pjm_manhattan.csv", header=False, index=False)
    if len(lic_classes) > 1:
        pd.DataFrame(lic_classes).to_csv(f"csv/{get_date()}/pjm_lic.csv", header=False, index=False)

    browser.quit()

if __name__ == '__main__':
    run()