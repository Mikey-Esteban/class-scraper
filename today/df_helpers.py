import pandas as pd
from datetime import datetime

def strip_time(df):
    df['Start time'] = df['Start time'].str.split('EDT').str[0]
    df['Start time'] = df['Start time'].replace(to_replace=r'(am|pm)', value=r'\1', regex=True)
    df['Start time'] = df['Start time'].replace(r' ', '', regex=True)
    return df

# def strip_time2(df):
#     time_str = df['Start time'].str.split('EST').str[0].to_string()
#     if time_str[-2:].lower() in ['am', 'pm'] and time_str.count(':') == 0:
#             time_str = time_str[:-2] + ':00' + time_str[-2:]
#     return datetime.strptime(time_str, '%I:%M%p').strftime('%I:%M%p')

def strip_time2(df):
    def reformat_time(time_str):
        # Remove EDT if present
        time_str = time_str.split('EDT')[0].strip()
        # Add ':00' if only the hour is provided
        if time_str[-2:].lower() in ['am', 'pm'] and time_str.count(':') == 0:
            time_str = time_str[:-2] + ':00' + time_str[-2:]
        # Try to parse with the desired formats
        time_formats = ['%I:%M%p', '%H:%M']
        for fmt in time_formats:
            try:
                # Try to parse the string with the current format
                return datetime.strptime(time_str, fmt).strftime('%I:%M%p')
            except ValueError:
                continue  # If parsing fails, try the next format
        # If none of the formats worked, print an error and return the original string
        print(f"Unable to parse time: {time_str}")
        return time_str  # or return some default value, or NaN, depending on your needs
    df['Start time'] = df['Start time'].apply(reformat_time)
    return df

def rename_columns(df):
    df = df.rename(columns={'Teacher': 'Instructor', 'Class': 'Classes', 'Class Schedule': 'Classes', 'Sessions': 'Classes', 'Link': 'Sign up'}, inplace=True)
    return df

def add_null_signups(df):
    df['Sign up'] = df.get('Sign up', 'none')   
    return df 

def shorten_class_level(df):
    df['Classes'] = df['Classes'].str.replace('beginner', 'Beg',case=False)
    df['Classes'] = df['Classes'].str.replace('foundations', 'Found',case=False)
    df['Classes'] = df['Classes'].str.replace('foundation', 'Found',case=False)
    df['Classes'] = df['Classes'].str.replace('introduction', 'Intro',case=False)
    df['Classes'] = df['Classes'].str.replace('intermediate', 'Int',case=False)
    df['Classes'] = df['Classes'].str.replace('inter', 'Int',case=False)
    df['Classes'] = df['Classes'].str.replace('advanced', 'Adv',case=False)
    return df

def change_hyphenation_of_class_level(df):
    df['Classes'] = df['Classes'].str.replace('Beg - Int', 'Beg/Int',case=False)
    df['Classes'] = df['Classes'].str.replace('Int - Beg', 'Int/Ben',case=False)
    df['Classes'] = df['Classes'].str.replace('Int - Adv', 'Int/Adv',case=False)
    df['Classes'] = df['Classes'].str.replace('Adv - Int', 'Adv/Int',case=False)
    return df

def remove_class_location(df):
    df['Classes'] = df['Classes'].str.replace('live-streaming', '',case=False)
    df['Classes'] = df['Classes'].str.replace('live-stream', '',case=False)
    df['Classes'] = df['Classes'].str.replace('livestream', '',case=False)
    df['Classes'] = df['Classes'].str.replace('live', '',case=False)
    df['Classes'] = df['Classes'].str.replace('in-studio', '',case=False)
    df['Classes'] = df['Classes'].str.replace('in-person', '',case=False)
    df['Classes'] = df['Classes'].str.replace('studio', '',case=False)
    df['Classes'] = df['Classes'].str.replace('online', '',case=False)
    df['Classes'] = df['Classes'].str.replace('virtual', '',case=False)
    df['Classes'] = df['Classes'].str.replace('lic', '',case=False)
    df['Classes'] = df['Classes'].str.replace('man', '',case=False)
    df['Classes'] = df['Classes'].str.replace(':', '',case=False)
    df['Classes'] = df['Classes'].str.replace('®', '',case=False)
    df['Classes'] = df['Classes'].str.replace('™', '',case=False)
    return df


def remove_instructor_from_class(df):
    df['Classes'] = df['Classes'].str.split('with').str[0]
    df['Classes'] = df['Classes'].str.split(' - ').str[0]
    return df

def remove_masks_from_instructor(df):
    df['Instructor'] = df['Instructor'].str.replace(r'\(masks optional\)','',case=False, regex=True)
    df['Instructor'] = df['Instructor'].str.replace(r'\(mask optional\)','',case=False, regex=True)
    df['Instructor'] = df['Instructor'].str.replace(r'\(masks required\)','',case=False, regex=True)
    df['Instructor'] = df['Instructor'].str.replace(r'\(mask required\)','',case=False, regex=True)
    return df

def remove_type_from_instructor(df):
    #Peridance
    df['Instructor'] = df['Instructor'].str.replace(r'^.+:', '', regex=True)
    df['Instructor'] = df['Instructor'].str.replace(r'\|.*$', '', regex=True)
    return df

def remove_quotes_from_instructor(df):
    df['Instructor'] = df['Instructor'].str.replace('"', '', case=False)
    return df

def remove_colon_from_class(df):
    # mark_morris has weird contemporary
    df['Classes'] = df['Classes'].str.replace('contemporary:', 'contemporary',case=False)
#     df['Classes'] = df['Classes'].str.split(':').str[1]
    df['Classes'] = df['Classes'].replace(r'^.+:', '', regex=True)
    return df

def remove_brackets_from_class(df):
    df['Classes'] = df['Classes'].str.replace('[()]', '', regex=True)
    df['Classes'] = df['Classes'].str.replace('[\[\]]', '', regex=True)
    return df

def shorten_class_style(df):
    df['Classes'] = df['Classes'].str.replace('contemporary', 'Contemp', case=False)
    df['Classes'] = df['Classes'].str.replace('commercial', 'Comm', case=False)
    df['Classes'] = df['Classes'].str.replace('choreography', 'Choreo', case=False)
    return df

def titleize_classes(df, series):
    df[series] = df[series].str.title()
    return df

def strip_df(df):
    return df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

def get_social_columns(df):
    return df[['Studio','Start time','Classes','Instructor','Sign up']]

def fix_ild_studios(filename, df):
    if filename == 'ild_nj.csv':
        df = df.replace('ILoveDance', 'ILD NJ')
    elif filename == 'ild_manhattan.csv':
        df = df.replace('ILoveDance', 'ILD NYC')
    elif filename == 'ild_queens.csv':
        df = df.replace('ILoveDance', 'ILD Queens')
    return df

def rename_columns_output(df):
    df = df.rename(columns={'Start time': 'Time'}, inplace=True)
    return df

def shorten_studios(df):
    df['Studio'] = df['Studio'].str.replace('Broadway Dance Center', 'BDC',case=False)
    df['Studio'] = df['Studio'].str.replace('Steps on Broadway', 'Steps',case=False)
    df['Studio'] = df['Studio'].str.replace('PMT House of Dance', 'PMT',case=False)
    df['Studio'] = df['Studio'].str.replace('PJM LIC', 'PJM',case=False)
    df['Studio'] = df['Studio'].str.replace('Gramercy Studios', 'Gramercy',case=False)
    df['Studio'] = df['Studio'].str.replace('Mark Morris Dance', 'Mark Morris',case=False)
    df['Studio'] = df['Studio'].str.replace('Ballet Academy East', 'BAE',case=False)
    df['Studio'] = df['Studio'].str.replace('Ailey Studios', 'Ailey',case=False)
    df['Studio'] = df['Studio'].str.replace('Cumbe Dance Center', 'Cumbe',case=False)
    df['Studio'] = df['Studio'].str.replace('Sass Class', 'SassClass',case=False)
    return df

def format_time(df):
    df['Start time'] = pd.to_datetime(df['Start time'],format= '%I:%M%p').dt.time
    return df