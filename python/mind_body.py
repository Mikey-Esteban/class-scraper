import os
import pandas as pd
from selenium import webdriver
from helpers import *
from studio import *

base_url = 'https://clients.mindbodyonline.com/classic/mainclass?studioid='

def run():
    for folder in ['live', 'virtual', 'social']:
        if not os.path.exists(f"csv/{get_date()}/{folder}"):
            os.makedirs(f"csv/{get_date()}/{folder}")

    for studio in studios:
        browser = webdriver.Firefox()
        browser.implicitly_wait(20)
        print('running for studio...', studio['name'])
        browser.get(f'{base_url}{studio["id"]}')

        func = studio['func']

        # for multiple tabs
        for index, tab_id in enumerate(studio['tab_ids']):
            if func.__name__ == 'run_full_week_csv':
                class_data = func(browser, tab_id, studio['table_name'], studio['date_format'])
            else:
                class_data = func(browser, tab_id, studio['table_name'])

            live, virtual = split_class_data(class_data)

            if len(live) > 1:
                pd.DataFrame(live).to_csv(f"csv/{get_date()}/live/{studio['filenames'][index]}", header=False, index=False)
            if len(virtual) > 1:
                pd.DataFrame(virtual).to_csv(f"csv/{get_date()}/virtual/{studio['filenames'][index]}", header=False, index=False)
        
        browser.quit()

if __name__ == '__main__':
    run()