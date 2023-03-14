import os
import pandas as pd
from selenium import webdriver
from helpers import *
import datetime
import time

base_url = 'https://sutrapro.com/modega'

def run():
    if not os.path.exists(f"csv/{get_date()}"):
        os.makedirs(f"csv/{get_date()}")

    # grab date in day 'Tuesday Mar 14th' format
    next_day_formatted = (date.today() + datetime.timedelta(days=1)).strftime('%A %b %d') + day_suffix((date.today() + datetime.timedelta(days=1)).day)

    browser = webdriver.Firefox()
    browser.implicitly_wait(20)
    browser.get(base_url)
    
    print('running for studio...', 'modega')
    correct_day_index = -1

    day_containers = browser.find_elements(By.CLASS_NAME, 'card-list__card-group')
    for i, day_container in enumerate(day_containers):
        if correct_day_index > -1: continue
        heading = day_container.find_element(By.CLASS_NAME, 'class-list__day')
        if (heading.text == next_day_formatted):
            correct_day_index = i

    classes_data = [['Time', 'Sign up', 'Class', 'Instructor']]
    classes_container = day_containers[correct_day_index].find_elements(By.CLASS_NAME, 'class-list__card')
    for class_container in classes_container:
        card = class_container.find_element(By.CLASS_NAME, 'card-body')
        time = card.find_element(By.CLASS_NAME, 'dateTimeText').text.strip()
        name = card.find_element(By.CLASS_NAME, 'card-title').text.strip()
        instructor_sign_up_div = card.find_element(By.CLASS_NAME, 'd-flex')
        instructor = instructor_sign_up_div.find_element(By.CLASS_NAME, 'card-text').text.strip()
        sign_up = instructor_sign_up_div.find_element(By.CLASS_NAME, 'ml-2').find_element(By.CLASS_NAME, 'btn').get_attribute('href')
        classes_data.append([time, sign_up, name, instructor])

    pd.DataFrame(classes_data).to_csv(f"csv/{get_date()}/modega.csv", header=False)

    browser.quit()

if __name__ == '__main__':
    run()