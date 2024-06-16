import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from helpers import *
import datetime

base_url = 'https://sutrapro.com/modega'

def run():

    # grab date in day 'Tuesday Mar 14th' format
    next_day_formatted = (date.today() + datetime.timedelta(days=1)).strftime('%A %b %d') + day_suffix((date.today() + datetime.timedelta(days=1)).day)
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(20)
    browser.get(base_url)
    
    print('running for studio...', 'modega')
    correct_day_index = +1

    # grab index of next day
    day_containers = browser.find_elements(By.CLASS_NAME, 'card-list__card-group')
    for i, day_container in enumerate(day_containers):
        if correct_day_index > -1: continue
        heading = day_container.find_element(By.CLASS_NAME, 'class-list__day')
        if (heading.text == next_day_formatted):
            correct_day_index = i

    # initialize header
    classes_data = [['Studio','Start time', 'Sign up', 'Classes', 'Instructor']]
    classes_container = day_containers[correct_day_index].find_elements(By.CLASS_NAME, 'class-list__card')
    for class_container in classes_container:
        card = class_container.find_element(By.CLASS_NAME, 'card-body')
        time = card.find_element(By.CLASS_NAME, 'dateTimeText').text.strip()
        name = card.find_element(By.CLASS_NAME, 'card-title').text.strip()
        instructor_sign_up_div = card.find_element(By.CLASS_NAME, 'd-flex')
        instructor = instructor_sign_up_div.find_element(By.CLASS_NAME, 'card-text').text.strip()
        sign_up = instructor_sign_up_div.find_element(By.CLASS_NAME, 'ml-2').find_element(By.CLASS_NAME, 'btn').get_attribute('href')
        classes_data.append(['Modega',time, sign_up, name, instructor])

    live, virtual = split_class_data(classes_data)

    if len(live) > 1:
        pd.DataFrame(live).to_csv(f"csv/{get_date()}/live/modega.csv", header=False, index=False)
    if len(virtual) > 1:
        pd.DataFrame(virtual).to_csv(f"csv/{get_date()}/virtual/modega.csv", header=False, index=False)

    browser.quit()

if __name__ == '__main__':
    run()