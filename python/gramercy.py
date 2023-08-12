import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from helpers import *
import datetime
import time

base_url = 'https://www.gramercydancestudios.com/schedule'

def run():

    # grab date in 'tuesday 3/14' format
    next_day_formatted = (date.today() + datetime.timedelta(days=1)).strftime('%A %-m/%d').lower()
    print(next_day_formatted)
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Firefox(options=options)
    browser.implicitly_wait(20)
    browser.get(base_url)
    
    print('running for studio...', 'gramercy')
    header_border_height = browser.find_element(By.CLASS_NAME, 'header-border').size['height']
    content_rows = browser.find_elements(By.CLASS_NAME, 'sqs-block-content')

    flag = False
    current_scroll = 0
    correct_date_index = -1

    content_rows = browser.find_elements(By.CLASS_NAME, 'fe-block')
    print('content rows len', len(content_rows))
    for i, row in enumerate(content_rows):
        if flag: continue
        browser.implicitly_wait(.1)

        try:
            h1 = row.find_element(By.TAG_NAME, 'h1')
            print('h1:', h1.text.lower())
            if h1.text.lower() != next_day_formatted: 
                # move to top of date
                top_of_date = browser.execute_script(f"return document.querySelectorAll('.fe-block')[{i}].getBoundingClientRect().top")
                current_scroll += top_of_date
                browser.execute_script(f"window.scrollTo(0,{current_scroll})")
                # move to bottom of date
                header_scroll_bottom = browser.execute_script(f"return document.querySelectorAll('.fe-block')[{i}].getBoundingClientRect().bottom")
                current_scroll += header_scroll_bottom
                browser.execute_script(f"window.scrollTo(0,{current_scroll})")
                # move to the top of the next element
                top_of_accordion = browser.execute_script(f"return document.querySelectorAll('.fe-block')[{i+1}].getBoundingClientRect().top")
                current_scroll += top_of_accordion
                browser.execute_script(f"window.scrollTo(0,{current_scroll})")
                # move to bottom of element
                bottom_of_accordion = browser.execute_script(f"return document.querySelectorAll('.fe-block')[{i+1}].getBoundingClientRect().bottom")
                current_scroll += bottom_of_accordion
                browser.execute_script(f"window.scrollTo(0,{current_scroll})")
                time.sleep(.2)
            else:
                correct_date_index = i + 1
                flag = True
        except:
            continue

    print('FOUND ACCORDION INDEX:', correct_date_index)
    correct_day_row = content_rows[correct_date_index]
    classes_for_date = correct_day_row.find_elements(By.TAG_NAME, 'li')
    print('classes length', len(classes_for_date))
    for thing in classes_for_date:
        split = thing.text.split('w/')
        if len(split) == 1:
            split = thing.text.split('W/')
        if len(split) == 1:
            split = thing.text.split('with')
        if len(split) == 1:
            split = thing.text.split('WITH')
        print(split)

        time_and_name = split[0].split(' ', 1)
        class_time = time_and_name[0]
        class_name = time_and_name[1]
        teacher = split[1]

    print(correct_day_row)
    correct_day_heading = correct_day_row.find_element(By.TAG_NAME, 'h4')
    correct_day_elements = correct_day_heading.find_elements(By.XPATH, ".//*")

    classes_data = [['Studio','Start time', 'Classes', 'Link', 'Instructor']]
    class_row = ['Gramercy Studios']
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
                class_row = ['Gramercy Studios']
            else:
                class_row.append(f'{stripped_text} {correct_day_elements[index + 1].text.strip()}')
        elif i == 3:
            class_row.append(el.get_attribute('href'))
        elif i == 4:
            class_row.append(stripped_text)
            classes_data.append(class_row)
            i = 0
            class_row = ['Gramercy Studios']

    live, virtual = split_class_data(classes_data)

    if len(live) > 1:
        pd.DataFrame(live).to_csv(f"csv/{get_date()}/live/gramercy.csv", header=False, index=False)
    if len(virtual) > 1:
        pd.DataFrame(virtual).to_csv(f"csv/{get_date()}/virtual/gramercy.csv", header=False, index=False)
    
    browser.quit()
        
if __name__ == '__main__':
    run()