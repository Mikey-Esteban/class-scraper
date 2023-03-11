import pandas as pd 
from selenium.webdriver.common.by import By
from helpers import *

def runAiley(browser):

    online_config = {
        'tabId': 'tabA111',
        'filename': 'ailey_online.csv'
    }

    inclass_config = {
        'tabId': 'tabA10',
        'filename': 'ailey_inclass.csv'
    }


    configs = [online_config, inclass_config]

    for config in configs:

        move_to_table(browser, config)

        even_rows = browser.find_elements(By.CLASS_NAME, 'evenRow')
        odd_rows = browser.find_elements(By.CLASS_NAME, 'oddRow')
        rows = even_rows + odd_rows

        class_data = []

        header_row = browser.find_elements(By.CLASS_NAME, 'floatingHeader-loaded')
        header_data = []
        for th in header_row:
            header_data.append('Sign up') if th.text == ' ' else header_data.append(th.text)

        class_data.append(header_data)

        class_data = get_class_data(rows, class_data)


        pd.DataFrame(class_data).to_csv(f"csv/{config['filename']}", header=False)  