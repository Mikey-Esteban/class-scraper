from selenium.webdriver.common.by import By

def move_to_table(browser, config):
    tab = browser.find_element(By.ID, config['tabId'])
    assert tab
    tab.click()

    today_button = browser.find_element(By.CLASS_NAME, 'today-button')
    assert today_button
    today_button.click()
    next_day_button = browser.find_element(By.ID, 'day-arrow-r')
    next_day_button.click()

def login(browser):
    input = browser.find_element(By.ID, 'su1UserName')
    password = browser.find_element(By.ID, 'su1Password')
    sign_in_button = browser.find_element(By.ID, 'btnSu1Login')

    input.send_keys('')
    password.send_keys('')

    sign_in_button.click()

def get_class_data(rows, class_data):

    # header_row = browser.find_elements(By.CLASS_NAME, 'floatingHeader-loaded')
    # header_data = []
    # for th in header_row:
    #     header_data.append('Sign up') if th.text == ' ' else header_data.append(th.text)

    # class_data.append(header_data)

    for row in rows:
        tds = row.find_elements(By.TAG_NAME, 'td')
        row_data = []
        for index, td in enumerate(tds):
            if index == 1:
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
            else:
                row_data.append(td.text)

        class_data.append(row_data)

    return class_data