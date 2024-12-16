import os
import pandas as pd
from datetime import datetime, date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import gspread
import csv
import re

shift_days = int(input("Enter 0 for today's classes, 1 for tomorrow's classes: ").strip())

def get_date():
    return (date.today() + timedelta(days=shift_days)).strftime("%Y%m%d")

def get_date2():
    return (date.today() + timedelta(days=shift_days)).strftime("%m/%d/%Y")

def day_suffix(myDate):
    date_suffix = ["th", "st", "nd", "rd"]
    if myDate % 10 in [1, 2, 3] and myDate not in [11, 12, 13]:
        return date_suffix[myDate % 10]
    else:
        return date_suffix[0]

def strip_time(df):
    if 'Start time' in df.columns:
        df['Start time'] = df['Start time'].str.replace('EDT', '', regex=False)
        df['Start time'] = df['Start time'].str.replace('EST', '', regex=False)
        df['Start time'] = df['Start time'].replace(to_replace=r'(am|pm)', value=r'\1', regex=True)
        df['Start time'] = df['Start time'].replace(r' ', '', regex=True)
    return df

def strip_time2(df):
    def reformat_time(time_str):
        if pd.isna(time_str):
            return time_str
        time_str = str(time_str).replace('EDT', '').replace('EST', '').strip()
        if len(time_str) > 2 and time_str[-2:].lower() in ['am', 'pm'] and ':' not in time_str:
            time_str = time_str[:-2] + ':00' + time_str[-2:]
        time_formats = ['%I:%M%p', '%H:%M']
        for fmt in time_formats:
            try:
                return datetime.strptime(time_str, fmt).strftime('%I:%M%p')
            except ValueError:
                continue
        print(f"Unable to parse time: {time_str}")
        return time_str
    if 'Start time' in df.columns:
        df['Start time'] = df['Start time'].apply(reformat_time)
    return df

def rename_columns(df):
    df.rename(columns={
        'Teacher': 'Instructor',
        'Class': 'Classes',
        'Class Schedule': 'Classes',
        'Sessions': 'Classes',
        'Link': 'Sign up'
    }, inplace=True)
    return df

def add_null_signups(df):
    df['Sign up'] = df.get('Sign up', 'none')
    return df

def shorten_class_level(df):
    replacements = {
        'beginner': 'Beg', 'foundations': 'Found', 'foundation': 'Found',
        'introduction': 'Intro', 'intermediate': 'Int', 'inter': 'Int',
        'advanced': 'Adv'
    }
    if 'Classes' in df.columns:
        for old, new in replacements.items():
            df['Classes'] = df['Classes'].str.replace(old, new, case=False)
    return df

def change_hyphenation_of_class_level(df):
    hyphenations = {
        'Beg - Int': 'Beg/Int',
        'Int - Beg': 'Int/Ben',
        'Int - Adv': 'Int/Adv',
        'Adv - Int': 'Adv/Int'
    }
    if 'Classes' in df.columns:
        for old, new in hyphenations.items():
            df['Classes'] = df['Classes'].str.replace(old, new, case=False)
    return df

def remove_class_location(df):
    if 'Classes' in df.columns:
        locations = ['live-streaming','live-stream','livestream','live','in-studio','in-person',
                     'studio','online','virtual','lic','man',':','®','™']
        for loc in locations:
            df['Classes'] = df['Classes'].str.replace(loc, '', case=False)
    return df

def remove_instructor_from_class(df):
    if 'Classes' in df.columns:
        df['Classes'] = df['Classes'].str.split('with').str[0]
        df['Classes'] = df['Classes'].str.split(' - ').str[0]
    return df

def remove_masks_from_instructor(df):
    if 'Instructor' in df.columns:
        patterns = [r'\(masks optional\)', r'\(mask optional\)', r'\(masks required\)', r'\(mask required\)']
        for p in patterns:
            df['Instructor'] = df['Instructor'].str.replace(p, '', case=False, regex=True)
    return df

def remove_type_from_instructor(df):
    if 'Instructor' in df.columns:
        df['Instructor'] = df['Instructor'].str.replace(r'^.+:', '', regex=True)
        df['Instructor'] = df['Instructor'].str.replace(r'\|.*$', '', regex=True)
    return df

def remove_quotes_from_instructor(df):
    if 'Instructor' in df.columns:
        df['Instructor'] = df['Instructor'].str.replace('"', '', case=False)
    return df

def remove_colon_from_class(df):
    if 'Classes' in df.columns:
        df['Classes'] = df['Classes'].str.replace('contemporary:', 'contemporary', case=False)
        df['Classes'] = df['Classes'].replace(r'^.+:', '', regex=True)
    return df

def remove_brackets_from_class(df):
    if 'Classes' in df.columns:
        df['Classes'] = df['Classes'].str.replace('[()]', '', regex=True)
        df['Classes'] = df['Classes'].str.replace('[\[\]]', '', regex=True)
    return df

def shorten_class_style(df):
    style_map = {'contemporary': 'Contemp', 'commercial': 'Comm', 'choreography': 'Choreo'}
    if 'Classes' in df.columns:
        for old, new in style_map.items():
            df['Classes'] = df['Classes'].str.replace(old, new, case=False)
    return df

def titleize_classes(df, series):
    if series in df.columns:
        df[series] = df[series].str.title()
    return df

def strip_df(df):
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    return df

def get_social_columns(df):
    return df[['Studio','Start time','Classes','Instructor','Sign up']]

def fix_ild_studios(filename, df):
    if filename == 'ild_nj.csv':
        df = df.replace('ILoveDance', 'ILD NJ')
    elif filename == 'ild_manhattan.csv':
        df = df.replace('ILoveDance', 'ILD NYC')
    elif filename == 'ild_queens.csv':
        df = df.replace('ILoveDance', 'ILD Queens')
    elif filename == 'ild_online.csv':
        df = df.replace('ILoveDance', 'ILD Online')
    return df

def rename_columns_output(df):
    if 'Start time' in df.columns:
        df.rename(columns={'Start time': 'Time'}, inplace=True)
    return df

def shorten_studios(df):
    studio_map = {
        'Broadway Dance Center': 'BDC',
        'Steps on Broadway': 'Steps',
        'PMT House of Dance': 'PMT',
        'PJM LIC': 'PJM',
        'Gramercy Studios': 'Gramercy',
        'Mark Morris Dance': 'Mark Morris',
        'Ballet Academy East': 'BAE',
        'Ailey Studios': 'Ailey',
        'Cumbe Dance Center': 'Cumbe',
        'Sass Class': 'SassClass'
    }
    if 'Studio' in df.columns:
        for old, new in studio_map.items():
            df['Studio'] = df['Studio'].str.replace(old, new, case=False)
    return df

def format_time(df):
    if 'Start time' in df.columns:
        df['Start time'] = pd.to_datetime(df['Start time'], format='%I:%M%p', errors='coerce').dt.time
    return df

def create_directories():
    for folder in ['live', 'virtual', 'counts', 'social', 'styles']:
        folder_path = f"csv/{get_date()}/{folder}"
        os.makedirs(folder_path, exist_ok=True)
    print("Directories created.")

def split_class_data(class_data):
    live_classes = [class_data[0]]
    virtual_classes = [class_data[0]]
    for i, row in enumerate(class_data):
        if i == 0:
            continue
        try:
            row_text = str(row[3]).lower()
            if any(x in row_text for x in ['virtual', 'online', 'livestream', 'live-']):
                virtual_classes.append(row)
            else:
                live_classes.append(row)
        except:
            continue
    return live_classes, virtual_classes

def scrape_studio(studio):
    base_url = 'https://clients.mindbodyonline.com/classic/mainclass?studioid='
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--headless')

    browser = webdriver.Chrome(options=options)
    total_live = 0
    total_virtual = 0

    def move_to_table(browser, tab_id):
        try:
            tab = browser.find_element(By.ID, tab_id)
            tab.click()
            today_button = browser.find_element(By.CLASS_NAME, 'today-button')
            today_button.click()
            if shift_days == 1:
                next_day_button = browser.find_element(By.ID, 'day-arrow-r')
                next_day_button.click()
            sleep(1)
        except Exception as e:
            print(f"Error moving to table: {e}")

def add_header(browser, class_data):
    header_row = browser.find_elements(By.CLASS_NAME, 'floatingHeader-loaded')
    header_data = ['Studio']
    for th in header_row:
        header_data.append('Sign up' if th.text.strip() == '' else th.text.strip())
    class_data.append(header_data)
    return class_data

def add_sign_up_link(td, row_data):
    try:
        sign_up_button = td.find_element(By.TAG_NAME, 'input')
        attribute = sign_up_button.get_attribute('onclick')
        attribute_array = attribute.split(' ')
        link = attribute_array[-2][1:-3]
        row_data.append(f'https://clients.mindbodyonline.com{link}')
    except:
        row_data.append('none')

def get_class_data(browser, rows, studio_name):
    class_data = add_header(browser, [])
    for row in rows:
        tds = row.find_elements(By.CLASS_NAME, 'col')
        row_data = [studio_name]
        for index, td in enumerate(tds):
            if index == 1:
                add_sign_up_link(td, row_data)
            else:
                val = td.text.strip()
                row_data.append(val if val else 'none')
        class_data.append(row_data)
    return class_data

def split_class_data(class_data):
    live_classes = [class_data[0]]
    virtual_classes = [class_data[0]]
    for i, row in enumerate(class_data):
        if i == 0:
            continue
        try:
            row_text = str(row[3]).lower()
            if any(x in row_text for x in ['virtual', 'online', 'livestream', 'live-']):
                virtual_classes.append(row)
            else:
                live_classes.append(row)
        except:
            continue
    return live_classes, virtual_classes

def move_to_table(browser, tab_id):
    try:
        tab = browser.find_element(By.ID, tab_id)
        tab.click()
        today_button = browser.find_element(By.CLASS_NAME, 'today-button')
        today_button.click()
        if shift_days == 1:
            next_day_button = browser.find_element(By.ID, 'day-arrow-r')
            next_day_button.click()
        sleep(1)
    except Exception as e:
        print(f"Error moving to table: {e}")

def run_full_week_csv(browser, tab_id, studio_name, date_format):
    target_day = date.today() + timedelta(days=shift_days)
    move_to_table(browser, tab_id)
    browser.implicitly_wait(.3)
    main_table = browser.find_element(By.ID, "classSchedule-mainTable")
    all_rows = main_table.find_elements(By.XPATH, "//*[@class='evenRow row' or @class='header' or @class='oddRow row']")
    correct_date_rows = []
    flag = False
    for row in all_rows:
        text = row.text.strip()
        try:
            date_formatted = datetime.strptime(text, date_format).date()
            if date_formatted == target_day:
                flag = True
            else:
                flag = False
        except:
            if flag:
                correct_date_rows.append(row)
    class_data = get_class_data(browser, correct_date_rows, studio_name)
    return class_data

def run_even_odds_csv(browser, tab_id, studio_name):
    move_to_table(browser, tab_id)
    even_rows = browser.find_elements(By.CLASS_NAME, 'evenRow')
    odd_rows = browser.find_elements(By.CLASS_NAME, 'oddRow')
    rows = even_rows + odd_rows
    class_data = get_class_data(browser, rows, studio_name)
    return class_data

studios = [
    {'name': 'aileystudios', 'table_name': 'Ailey Studios', 'id': '851', 'tab_ids': ['tabA10', 'tabA111'], 'func': run_even_odds_csv, 'filenames': ['ailey.csv', 'ailey.csv']},
    {'name': 'atdf', 'table_name': 'ATDF', 'id': '14721', 'tab_ids': ['tabA118'], 'func': run_full_week_csv, 'date_format': '%a %B %d, %Y', 'filenames': ['atdf.csv']},
    {'name': 'balletacademyeast', 'table_name': 'Ballet Academy East', 'id': '30500', 'tab_ids': ['tabA7'], 'func': run_full_week_csv, 'date_format': '%A %B %d, %Y', 'filenames': ['ballet_academy_east.csv']},
    {'name': 'balletarts', 'table_name': 'Ballet Arts', 'id': '589886', 'tab_ids': ['tabA7'], 'func': run_even_odds_csv, 'filenames': ['ballet_arts.csv']},
    {'name': 'broadwaydancecenter', 'table_name': 'Broadway Dance Center', 'id': '28329', 'tab_ids': ['tabA7'], 'func': run_even_odds_csv, 'filenames': ['bdc.csv']},
    {'name': 'brickhouse', 'table_name': 'Brickhouse', 'id': '807568', 'tab_ids': ['tabA7'], 'func': run_full_week_csv, 'date_format': '%A %B %d, %Y', 'filenames': ['brickhouse.csv']},
    {'name': 'cumbe', 'table_name': 'Cumbe Dance Center', 'id': '16827', 'tab_ids': ['tabA112', 'tabA111'], 'func': run_full_week_csv, 'date_format': '%a %B %d, %Y', 'filenames': ['cumbe.csv', 'cumbe.csv']},
    {'name': 'gibney', 'table_name': 'Gibney', 'id': '31459', 'tab_ids': ['tabA7'], 'func': run_full_week_csv, 'date_format': '%a %B %d, %Y', 'filenames': ['gibney.csv']},
    {'name': 'ild', 'table_name': 'ILoveDance', 'id': '144750', 'tab_ids': ['tabA104', 'tabA103', 'tabA102', 'tabA105'], 'func': run_full_week_csv, 'date_format': '%a %B %d, %Y', 'filenames': ['ild_manhattan.csv', 'ild_nj.csv', 'ild_queens.csv', 'ild_online.csv']},
    {'name': 'markmorris', 'table_name': 'Mark Morris Dance', 'id': '95201', 'tab_ids': ['tabA7'], 'func': run_full_week_csv, 'date_format': '%a %B %d, %Y', 'filenames': ['mark_morris.csv']},
    {'name': 'peridance', 'table_name': 'Peridance', 'id': '38909', 'tab_ids': ['tabA125'], 'func': run_full_week_csv, 'date_format': '%a %B %d, %Y', 'filenames': ['peridance.csv']},
    {'name': 'pmt', 'table_name': 'PMT House of Dance', 'id': '727061', 'tab_ids': ['tabA7'], 'func': run_full_week_csv, 'date_format': '%A %B %d, %Y', 'filenames': ['pmt.csv']},
    {'name': 'sass', 'table_name': 'Sass Class', 'id': '988409', 'tab_ids': ['tabA103', 'tabA106'], 'func': run_full_week_csv, 'date_format': '%a %B %d, %Y', 'filenames': ['sass.csv', 'sass.csv']},
    {'name': 'steps', 'table_name': 'Steps on Broadway', 'id': '-308', 'tab_ids': ['tabA107', 'tabA109'], 'func': run_full_week_csv, 'date_format': '%A %B %d, %Y', 'filenames': ['steps.csv', 'steps.csv']},
    {'name': 'taylor', 'table_name': 'Taylor School', 'id': '463013', 'tab_ids': ['tabA7'], 'func': run_full_week_csv, 'date_format': '%a %B %d, %Y', 'filenames': ['taylor.csv']},
    {'name': 'thehive', 'table_name': 'Hive NJ', 'id': '642345', 'tab_ids': ['tabA7'], 'func': run_full_week_csv, 'date_format': '%a %B %d, %Y', 'filenames': ['thehive.csv']},
    {'name': 'thefemmily', 'table_name': 'Femmily', 'id': '5735205', 'tab_ids': ['tabA7'], 'func': run_full_week_csv, 'date_format': '%a %B %d, %Y', 'filenames': ['thefemmily.csv']}
]

class_counts = []

def scrape_studio(studio):
    base_url = 'https://clients.mindbodyonline.com/classic/mainclass?studioid='
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    browser = webdriver.Chrome(options=options)
    total_live = 0
    total_virtual = 0

    try:
        browser.get(f"{base_url}{studio['id']}")
        wait = WebDriverWait(browser, 20)
        
        for index, tab_id in enumerate(studio['tab_ids']):
            wait.until(EC.element_to_be_clickable((By.ID, tab_id))).click()
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'row')))

            if studio['func'] == run_even_odds_csv:
                class_data = run_even_odds_csv(browser, tab_id, studio['table_name'])
            else:
                class_data = studio['func'](browser, tab_id, studio['table_name'], studio['date_format'])

            live, virtual = split_class_data(class_data)

            if len(live) > 1:
                live_path = f"csv/{get_date()}/live/{studio['filenames'][index]}"
                pd.DataFrame(live).to_csv(live_path, index=False, header=False)
                total_live += (len(live) - 1)
            if len(virtual) > 1:
                virtual_path = f"csv/{get_date()}/virtual/{studio['filenames'][index]}"
                pd.DataFrame(virtual).to_csv(virtual_path, index=False, header=False)
                total_virtual += (len(virtual) - 1)

        class_counts.append({
            'Studio': studio['table_name'],
            'Date': get_date2(),
            'Live Classes': total_live,
            'Virtual Classes': total_virtual,
            'Total Classes': total_live + total_virtual
        })
        
        print(f"Live: {total_live:<3} | Virtual: {total_virtual:<3} | Studio: {studio['table_name']}")
    except Exception as e:
        print(f"Error scraping studio {studio['name']}: {e}")
    finally:
        browser.quit()

def run_modega():
    base_url = 'https://sutrapro.com/modega'
    target_day = date.today() + timedelta(days=shift_days)
    next_day_formatted = target_day.strftime('%A %b %d') + day_suffix(target_day.day)

    options = Options()
    # options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(20)
    print('running for studio...', 'modega')
    browser.get(base_url)
    sleep(2)
    day_containers = browser.find_elements(By.CLASS_NAME, 'card-list__card-group')
    correct_day_index = -1
    for i, day_container in enumerate(day_containers):
        heading = day_container.find_element(By.CLASS_NAME, 'class-list__day')
        if heading.text.strip().lower() == next_day_formatted.lower():
            correct_day_index = i
            break
    classes_data = [['Studio', 'Sign up', 'Start time', 'Classes', 'Instructor']]
    if correct_day_index != -1:
        classes_container = day_containers[correct_day_index].find_elements(By.CLASS_NAME, 'class-list__card')
        for class_container in classes_container:
            card = class_container.find_element(By.CLASS_NAME, 'card-body')
            raw_time = card.find_element(By.CLASS_NAME, 'dateTimeText').text.strip()
            if '•' in raw_time:
                raw_time = raw_time.split('•')[0].strip()
            raw_time = raw_time.replace("EST", "").strip()
            raw_time = re.sub(r'\s+(AM|PM)$', r'\1', raw_time, flags=re.IGNORECASE)
            raw_time = raw_time.replace(" ", "")
            name = card.find_element(By.CLASS_NAME, 'card-title').text.strip()
            instructor_sign_up_div = card.find_element(By.CLASS_NAME, 'd-flex')
            instructor = instructor_sign_up_div.find_element(By.CLASS_NAME, 'card-text').text.strip()
            sign_up = instructor_sign_up_div.find_element(By.CLASS_NAME, 'ml-2').find_element(By.CLASS_NAME, 'btn').get_attribute('href')
            classes_data.append(['Modega', sign_up, raw_time, name, instructor])
    browser.quit()
    live, virtual = split_class_data(classes_data)
    total_live = len(live) - 1 if len(live) > 1 else 0
    total_virtual = len(virtual) - 1 if len(virtual) > 1 else 0
    if len(live) > 1:
        pd.DataFrame(live).to_csv(f"csv/{get_date()}/live/modega.csv", header=False, index=False)
    if len(virtual) > 1:
        pd.DataFrame(virtual).to_csv(f"csv/{get_date()}/virtual/modega.csv", header=False, index=False)
    print(f"Live: {total_live:<3} | Virtual: {total_virtual:<3} | Studio: Modega")

def run_pjm():
    base_url = 'https://www.versd.co/profile/pjm'
    target_day = date.today() + timedelta(days=shift_days)
    next_day_formatted = target_day.strftime('%A %B %d, %Y')

    options = Options()
    # options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(20)

    print('running for studio...', 'PJM')
    browser.get(base_url)
    sleep(2)

    classes_data = [['Studio', 'Sign up', 'Start time', 'Classes', 'Instructor']]
    class_blocks = browser.find_elements(By.XPATH, '//a[contains(@href, "/listing/")]/ancestor::div[@class="_ai-stretch _dsp-flex _fd-column _fb-auto _bxs-border-box _pos-relative"]')

    for block in class_blocks:
        class_link_el = block.find_element(By.XPATH, './/a[contains(@href, "/listing/") and h2]')
        class_name = class_link_el.find_element(By.TAG_NAME, 'h2').text.strip()
        listing_href = class_link_el.get_attribute('href')
        sign_up_link = listing_href if listing_href.startswith('http') else ('https://www.versd.co' + listing_href)
        
        # Extract teacher name:
        h3s = block.find_elements(By.TAG_NAME, 'h3')
        teacher_name = 'none'
        for i, h3_el in enumerate(h3s):
            if 'Teacher:' in h3_el.text:
                if i+1 < len(h3s):
                    teacher_name = h3s[i+1].text.strip()
                break

        # Extract start time:
        ps = block.find_elements(By.TAG_NAME, 'p')
        start_time = 'none'
        for i, p_el in enumerate(ps):
            text = p_el.text.strip()
            if ' to ' in text.lower():
                start_part = text.lower().split('to')[0].strip()
                # Determine am/pm from next element if needed:
                if i+1 < len(ps):
                    end_part = ps[i+1].text.strip()
                    ampm = 'AM' if 'am' in end_part.lower() else 'PM'
                    start_time = start_part
                    if not re.search(r'(am|pm)$', start_time.lower()):
                        start_time += ampm
                break

        classes_data.append(['PJM', sign_up_link, start_time, class_name, teacher_name])

    browser.quit()

    # Split class data into live and virtual
    live, virtual = split_class_data(classes_data)
    total_live = len(live) - 1 if len(live) > 1 else 0
    total_virtual = len(virtual) - 1 if len(virtual) > 1 else 0

    if len(live) > 1:
        pd.DataFrame(live).to_csv(f"csv/{get_date()}/live/pjm.csv", header=False, index=False)
    if len(virtual) > 1:
        pd.DataFrame(virtual).to_csv(f"csv/{get_date()}/virtual/pjm.csv", header=False, index=False)

    print(f"Live: {total_live:<3} | Virtual: {total_virtual:<3} | Studio: PJM")


def run_hoboken():
    # The Studio at Hoboken
    target_day = date.today() + timedelta(days=shift_days)
    dt_param = target_day.strftime("%Y-%m-%d")
    base_url = f"https://www.wellnessliving.com/rs/schedule/the_studio_at_hoboken?k_business=318213&k_class_tab=51998&id_class_tab=1#dt_date={dt_param}"

    options = Options()
    # options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(20)

    print('running for studio...', 'The Studio at Hoboken')
    browser.get(base_url)
    sleep(2)

    classes_data = [['Studio', 'Sign up', 'Start time', 'Classes', 'Instructor']]
    class_rows = browser.find_elements(By.CSS_SELECTOR, '.css-schedule-class-row.js-schedule-item-')

    for row in class_rows:
        try:
            time_el = row.find_element(By.CSS_SELECTOR, '.css-schedule-class-time span')
            raw_time = time_el.text.strip()
            start_time = raw_time.split('-')[0].strip()

            class_link = row.find_element(By.CSS_SELECTOR, '.css-schedule-class-name .js-schedule-list-class-info')
            class_name = class_link.text.strip()
            sign_up = class_link.get_attribute('href')

            instructor_el = row.find_element(By.CSS_SELECTOR, '.css-schedule-class-staff-wrapper a')
            instructor = instructor_el.text.strip()

            studio = 'The Studio at Hoboken NJ'
            classes_data.append([studio, sign_up, start_time, class_name, instructor])

        except Exception as e:
            print(f"Error parsing a row: {e}")
            continue

    browser.quit()

    # Split class data into live and virtual
    live, virtual = split_class_data(classes_data)
    total_live = len(live) - 1 if len(live) > 1 else 0
    total_virtual = len(virtual) - 1 if len(virtual) > 1 else 0

    if len(live) > 1:
        pd.DataFrame(live).to_csv(f"csv/{get_date()}/live/hoboken.csv", index=False, header=False)
    if len(virtual) > 1:
        pd.DataFrame(virtual).to_csv(f"csv/{get_date()}/virtual/hoboken.csv", index=False, header=False)

    print(f"Live: {total_live:<3} | Virtual: {total_virtual:<3} | Studio: The Studio at Hoboken")

def create_social_csv():
    path = f'./csv/{get_date()}/live'
    w_path = f'./csv/{get_date()}/social'
    if not os.path.exists(w_path):
        os.makedirs(w_path)
    files = os.listdir(path)
    for f in files:
        df = pd.read_csv(f'{path}/{f}', index_col=False)
        df = fix_ild_studios(f, df)
        strip_time(df)
        strip_time2(df)
        rename_columns(df)
        add_null_signups(df)
        remove_colon_from_class(df)
        remove_brackets_from_class(df)
        remove_class_location(df)
        remove_quotes_from_instructor(df)
        remove_type_from_instructor(df)
        shorten_class_level(df)
        change_hyphenation_of_class_level(df)
        remove_instructor_from_class(df)
        remove_masks_from_instructor(df)
        shorten_class_style(df)
        titleize_classes(df, 'Classes')
        shorten_studios(df)
        format_time(df)
        df = df.dropna()
        df = get_social_columns(strip_df(df))
        df.to_csv(f'{w_path}/{f}', index=False)

def categorize():
    path = f'./csv/{get_date()}/social'
    styles_path = f'./csv/{get_date()}/styles'
    if not os.path.exists(styles_path):
        os.makedirs(styles_path)
    files = os.listdir(path)
    tap, theater, ballet, contemporary_modern, street_styles_choreography, jazz, world_dance, other = ([] for _ in range(8))
    is_tap = ['tap']
    is_theater = ['theater','broadway']
    is_ballet = ['ballet','pointe','barre','ballez']
    is_contemporary_modern = ['contemp','modern','horton','graham','dunham','limón','cunningham','gaga','lyrical','empowered expression']
    is_street = ['hip hop', 'hip-hop', 'tutting', 'heels', 'styling free','stilettos','popping','breaking','jerz','jersey','locking','house','street','urban','chairography','vogue','choreo','pop up','funk','wacking','waacking','grooves','fusion','hustle','breakin','modega','voguing','litefeet','expressive','krump','shapes','master','battle','jen bayan','pop-up','freestyle session','waving']
    is_jazz = ['jazz']
    is_world = ['salsa','afro','african','dancehall','reggaeton','congolese','sabar','haitian','mambo','samba','bhangra','capoeira','latin','guinean','indian','flamenco','senegalese']
    all_styles = [is_tap, is_theater, is_ballet, is_contemporary_modern, is_street, is_jazz, is_world]
    for f in files:
        df = pd.read_csv(f'{path}/{f}', index_col=False)
        if 'Classes' not in df.columns or 'Studio' not in df.columns:
            continue
        for _, line in df.iterrows():
            studio = str(line['Studio']).lower()
            class_val = line['Classes']
            if not isinstance(class_val, str):
                other.append(line)
                continue
            class_name = class_val.lower()
            if studio == 'atdf':
                tap.append(line)
                continue
            if any(x in class_name for x in ['private', 'rehearsal', 'auditions']):
                continue
            style_found = False
            for style in all_styles:
                if style_found:
                    break
                for name in style:
                    if name in class_name:
                        if style == is_tap:
                            tap.append(line)
                        elif style == is_theater:
                            theater.append(line)
                        elif style == is_ballet:
                            ballet.append(line)
                        elif style == is_contemporary_modern:
                            contemporary_modern.append(line)
                        elif style == is_street:
                            street_styles_choreography.append(line)
                        elif style == is_jazz:
                            jazz.append(line)
                        elif style == is_world:
                            world_dance.append(line)
                        style_found = True
                        break
            if not style_found:
                print('did not find style', class_name)
                other.append(line)
    def process_df(df, style_name, fname):
        if not df.empty:
            rename_columns_output(df)
            current_date = pd.Timestamp(get_date2()).strftime('%m/%d')
            # current_date = pd.Timestamp(get_date2())
            df['Date'] = current_date
            df['Style'] = style_name
            if 'Time' in df.columns:
                df.sort_values(by='Time', inplace=True)
            df.to_csv(f'{styles_path}/{fname}.csv', index=False, header=False)
            return df
        else:
            return pd.DataFrame()
    street_df = process_df(pd.DataFrame(street_styles_choreography),'Street/Choreography','street_styles_choreography')
    ballet_df = process_df(pd.DataFrame(ballet),'Ballet','ballet')
    contemporary_modern_df = process_df(pd.DataFrame(contemporary_modern),'Contemporary/Modern','contemporary_modern')
    jazz_df = process_df(pd.DataFrame(jazz),'Jazz','jazz')
    tap_df = process_df(pd.DataFrame(tap),'Tap','tap')
    theater_df = process_df(pd.DataFrame(theater),'Theater','theater')
    world_df = process_df(pd.DataFrame(world_dance),'World','world')
    other_df = process_df(pd.DataFrame(other),'Additional Disciplines','additional_disciplines')
    all_frames = [x for x in [street_df, ballet_df, contemporary_modern_df, jazz_df, tap_df, theater_df, world_df, other_df] if not x.empty]
    if all_frames:
        all_df = pd.concat(all_frames)
        if 'Time' in all_df.columns:
            all_df.sort_values(by='Time', inplace=True)
        all_df.to_csv(f'{styles_path}/all.csv', index=False, header=True)

def csv_to_gs():
    gc = gspread.oauth()
    if shift_days == 0:
        spreadsheetId_all = '1VcJOUVp-i0i1bw-hK8fhGZTdS3U1-LSFMwbTCQQjN5c'
        spreadsheetId_tabbed = '1ptMefNH6sGm83zTo0S4KiVs83A4znzKPXFR7cs-3EeQ'
    else:
        spreadsheetId_all = '1HEVy5YVR6hVyK7UuiiEIL_luQYNG2kAcBrpZHA5EuDA'
        spreadsheetId_tabbed = '1etM9aRp0MDspxHVqQQ7u-TJCmi9HvruoZXX0QGG_6jg'
    sheetName = 'All'
    csvFile = f'csv/{get_date()}/styles/all.csv'
    if os.path.exists(csvFile):
        sh = gc.open_by_key(spreadsheetId_all)
        sh.values_clear(sheetName)
        sh.values_update(
            sheetName,
            params={'valueInputOption': 'USER_ENTERED'},
            body={'values': list(csv.reader(open(csvFile)))}
        )
    mapping = {
        'Street_Data': 'street_styles_choreography.csv',
        'Contemp_Data': 'contemporary_modern.csv',
        'Jazz_Data': 'jazz.csv',
        'Theater_Data': 'theater.csv',
        'Ballet_Data': 'ballet.csv',
        'Tap_Data': 'tap.csv',
        'World_Data': 'world.csv',
        'Other_Data': 'additional_disciplines.csv'
    }
    for sheetName, fileName in mapping.items():
        csvFile = f'csv/{get_date()}/styles/{fileName}'
        if os.path.exists(csvFile):
            sh = gc.open_by_key(spreadsheetId_tabbed)
            sh.values_clear(sheetName)
            sh.values_update(
                sheetName,
                params={'valueInputOption': 'USER_ENTERED'},
                body={'values': list(csv.reader(open(csvFile)))}
            )

class_counts = []

def save_class_counts():
    if class_counts:
        df_counts = pd.DataFrame(class_counts)
        df_counts.to_csv(f'csv/{get_date()}/counts/class_counts.csv', index=False)
        print("Class counts saved.")

def run():
    create_directories()
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(scrape_studio, studios)
    run_modega()
    run_pjm()
    run_hoboken()
    create_social_csv()
    categorize()
    csv_to_gs()
    save_class_counts()
    if class_counts:
        total_classes = sum(item['Total Classes'] for item in class_counts)
        print(f"Total classes pulled: {total_classes}")

if __name__ == "__main__":
    run()
