import pandas as pd
from selenium import webdriver
from helpers import *
import datetime
import time

base_url = 'https://www.gramercydancestudios.com/schedule'

def run():

    # grab date in 'tuesday 3/14' format
    next_day_formatted = (date.today() + datetime.timedelta(days=1)).strftime('%A %-m/%d').lower()
 
    browser = webdriver.Firefox()
    browser.implicitly_wait(20)
    browser.get(base_url)
    
    print('running for studio...', 'gramercy')
    header_border_height = browser.find_element(By.CLASS_NAME, 'header-border').size['height']
    content_rows = browser.find_elements(By.CLASS_NAME, 'sqs-block-content')

    flag = False
    currrent_scroll = 0
    correct_date_index = -1

    # scroll until date is found
    for i, row in enumerate(content_rows):
        if flag: continue

        # move scroll to next date header
        if (row.text.strip().lower().split(' ')[0] in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']):
            scroll_height = browser.execute_script(f"return document.querySelectorAll('.sqs-block-content')[{i}].getBoundingClientRect().top")
            currrent_scroll += scroll_height - header_border_height
            browser.execute_script(f"window.scrollTo(0,{currrent_scroll})")
            time.sleep(.3)

            # date is found
            if row.text.strip().lower() == next_day_formatted: 
                flag = True
                correct_date_index = i + 1

    correct_day_row = content_rows[correct_date_index]
    correct_day_heading = correct_day_row.find_element(By.TAG_NAME, 'h4')
    correct_day_elements = correct_day_heading.find_elements(By.XPATH, ".//*")

    classes_data = [['Start time', 'Classes', 'Link', 'Instructor']]
    class_row = []
    i = 0

    # rows work in blocks of 4, skip empty content
    for index, el in enumerate(correct_day_elements):
        if el.text.strip() == '': continue

        stripped_text = el.text.strip()
        i += 1
        if i == 1:
            class_row.append(stripped_text)
        elif i == 2:
            # reset everything
            if (stripped_text == 'available for rentals'):
                i = 0
                class_row = []
            else:
                class_row.append(f'{stripped_text} {correct_day_elements[index + 1].text.strip()}')
        elif i == 3:
            class_row.append(el.get_attribute('href'))
        elif i == 4:
            class_row.append(stripped_text)
            classes_data.append(class_row)
            i = 0
            class_row = []

    live, virtual = split_class_data(classes_data)

    if len(live) > 1:
        pd.DataFrame(live).to_csv(f"csv/{get_date()}/live/gramercy.csv", header=False, index=False)
    if len(virtual) > 1:
        pd.DataFrame(virtual).to_csv(f"csv/{get_date()}/virtual/gramercy.csv", header=False, index=False)
    
    browser.quit()
        
if __name__ == '__main__':
    run()