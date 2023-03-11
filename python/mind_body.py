from selenium import webdriver

from helpers import *

from ailey import *
from atdf import *

 
studios = [
    {'name': 'aileystudios', 'id':'851', 'func': runAiley},
    {'name': 'atdf', 'id':'14721', 'func': runAtdf},
]

base_url = 'https://clients.mindbodyonline.com/classic/mainclass?studioid='

browser = webdriver.Firefox()

def run():
    browser.implicitly_wait(10)

    for studio in studios:
        print('running for studio...', studio['name'])
        browser.get(f'{base_url}{studio["id"]}')

        func = studio['func']
        func(browser)
        
    browser.quit()
        

if __name__ == '__main__':
    run()