import os
import pandas as pd
from selenium import webdriver
from helpers import *
from studio import *

base_url = 'https://clients.mindbodyonline.com/classic/mainclass?studioid='

def run():
    if not os.path.exists(f"csv/{get_date()}"):
        os.makedirs(f"csv/{get_date()}")

    for studio in studios:
        browser = webdriver.Firefox()
        browser.implicitly_wait(20)
        print('running for studio...', studio['name'])
        browser.get(f'{base_url}{studio["id"]}')

        func = studio['func']

        for index, tab_id in enumerate(studio['tab_ids']):
            if func.__name__ == 'run_full_week_csv':
                class_data = func(browser, tab_id, studio['date_format'])
            else:
                class_data = func(browser, tab_id)

            pd.DataFrame(class_data).to_csv(f"csv/{get_date()}/{studio['filenames'][index]}", header=False, index=False)
        
        browser.quit()
        

if __name__ == '__main__':
    run()