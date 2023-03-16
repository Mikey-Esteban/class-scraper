import pandas as pd
from selenium import webdriver
from helpers import *
import datetime

base_url = 'https://www.pjmstudionyc.com/'

def isManhattan(str):
    return str == '[MAN]'

def run():

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

    manhattan_classes = [['Start time', 'Classes', 'Instructor', 'Length']]
    lic_classes = [['Start time', 'Classes', 'Instructor', 'Length']]

    correct_date_container = dates_rows[correct_date_index]
    correct_date_row = correct_date_container.find_element(By.CLASS_NAME, 'sLoech5')
    classes_rows = correct_date_row.find_elements(By.CLASS_NAME, 'sYbjzkn')
    for class_row in classes_rows:
        class_data = class_row.text.split('\n')[:4]
        if isManhattan(class_data[1].split(' ')[0]):
            manhattan_classes.append(class_data)
        else:
            lic_classes.append(class_data)

    live_man, virtual_man = split_class_data(manhattan_classes)
    live_lic, virtual_lic = split_class_data(lic_classes)

    if len(live_man) > 1:
        pd.DataFrame(live_man).to_csv(f"csv/{get_date()}/live/pjm_manhattan.csv", header=False, index=False)
    if len(virtual_man) > 1:
        pd.DataFrame(virtual_man).to_csv(f"csv/{get_date()}/virtual/pjm_manhattan.csv", header=False, index=False)

    if len(live_lic) > 1:
        pd.DataFrame(live_lic).to_csv(f"csv/{get_date()}/live/pjm_lic.csv", header=False, index=False)
    if len(virtual_lic) > 1:
        pd.DataFrame(virtual_lic).to_csv(f"csv/{get_date()}/virtual/pjm_lic.csv", header=False, index=False)

    browser.quit()

if __name__ == '__main__':
    run()