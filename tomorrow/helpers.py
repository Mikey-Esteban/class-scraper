from selenium.webdriver.common.by import By
from datetime import date
import datetime

#TODO - update get_date in each scraper (not all variable-based)
#For each data-pull, modify categorize.py & to place the files in the correct folder path. Scraper must be run on the day prior.
#Data pull must be done on prior day (./script.sh)
#To place a prior day's data pull into today (e.g., after midnight), modify categorize.py and csv_to_gs.py to send the correct date

#Use get_date() for tomorrow's date
def get_date():
    return (date.today() + datetime.timedelta(days=1)).strftime("%Y%m%d")
#Use get_date2() for labeling the table, categorize line 111 - 118 for tomorrow's date
def get_date2():
    return (date.today() + datetime.timedelta(days=1)).strftime("%m/%d/%Y")

#Use get_date3() for today's date
def get_date3():
    return (date.today().strftime("%Y%m%d"))

#Use get_date4() for labeling the table, categorize line 111 - 118 for today's date
def get_date4():
    return (date.today().strftime("%m/%d/%Y"))

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
    header_data = ['Studio']
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
        row_data.append(f'https://clients.mindbodyonline.com{link}')
    except:
        row_data.append('none')


def get_class_data(browser, rows, studio_name):
    
    class_data = add_header(browser, [])

    for row in rows:
        tds = row.find_elements(By.TAG_NAME, 'td')
        row_data = [studio_name]
        for index, td in enumerate(tds):
            if index == 1:
                add_sign_up_link(td, row_data)
            else:
                row_data.append('none') if td.text.strip() == '' else row_data.append(td.text.strip())

        class_data.append(row_data)
    
    return class_data

def split_class_data(class_data):
    # include header
    live_classes = [class_data[0]]
    virtual_classes = [class_data[0]]

    for i,row in enumerate(class_data):
        #skip header
        if i == 0:
            continue
        try:
            # class is 4th column
            row_text = row[3].lower()
            if 'virtual' in row_text or 'online' in row_text or 'livestream' in row_text or 'live-' in row_text:
                virtual_classes.append(row)
            else:
                live_classes.append(row)
        except:
            continue

    return live_classes, virtual_classes