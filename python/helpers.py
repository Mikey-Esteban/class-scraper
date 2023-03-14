from selenium.webdriver.common.by import By
from datetime import date
import datetime

def get_date():
    return (date.today() + datetime.timedelta(days=1)).strftime("%d_%m_%Y")

def day_suffix(myDate):
    date_suffix = ["th", "st", "nd", "rd"]

    if myDate % 10 in [1, 2, 3] and myDate not in [11, 12, 13]:
        return date_suffix[myDate % 10]
    else:
        return date_suffix[0]

def move_to_table(browser, tab_id):
    browser.implicitly_wait(20)
    tab = browser.find_element(By.ID, tab_id)
    assert tab
    tab.click()

    today_button = browser.find_element(By.CLASS_NAME, 'today-button')
    assert today_button
    today_button.click()
    next_day_button = browser.find_element(By.ID, 'day-arrow-r')
    next_day_button.click()
    browser.implicitly_wait(1)

def login(browser):
    input = browser.find_element(By.ID, 'su1UserName')
    password = browser.find_element(By.ID, 'su1Password')
    sign_in_button = browser.find_element(By.ID, 'btnSu1Login')

    input.send_keys('')
    password.send_keys('')

    sign_in_button.click()

def add_header(browser, class_data):
    header_row = browser.find_elements(By.CLASS_NAME, 'floatingHeader-loaded')
    header_data = []
    for th in header_row:
        header_data.append('Sign up') if th.text == ' ' else header_data.append(th.text)

    class_data.append(header_data)

    return class_data

def add_sign_up_link(td, row_data):
    try:
        sign_up_button = td.find_element(By.TAG_NAME, 'input')
        attribute = sign_up_button.get_attribute('onclick')
        attribute_array = attribute.split(' ')
        # get hyperlink
        link = attribute_array[len(attribute_array) - 2]
        link = link[1:-3]
        row_data.append(link)
    except:
        row_data.append('none')


def get_class_data(browser, rows):
    
    class_data = add_header(browser, [])

    for row in rows:
        tds = row.find_elements(By.TAG_NAME, 'td')
        row_data = []
        for index, td in enumerate(tds):
            if index == 1:
                add_sign_up_link(td, row_data)
            else:
                row_data.append('none') if td.text.strip() == '' else row_data.append(td.text.strip())

        class_data.append(row_data)

    return class_data