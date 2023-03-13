from selenium.webdriver.common.by import By
from helpers import *

def run_even_odds_csv(browser, tab_id):

    move_to_table(browser, tab_id)

    even_rows = browser.find_elements(By.CLASS_NAME, 'evenRow')
    odd_rows = browser.find_elements(By.CLASS_NAME, 'oddRow')
    rows = even_rows + odd_rows

    class_data = get_class_data(browser, rows)

    return class_data