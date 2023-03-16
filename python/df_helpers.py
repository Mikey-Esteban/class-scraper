def shorten_class_level(df):
    df['Classes'] = df['Classes'].str.replace('^beginn$', 'Beg', regex=True, case=False)
    df['Classes'] = df['Classes'].str.replace('^inter$', 'Int', regex=True, case=False)
    df['Classes'] = df['Classes'].str.replace('^advanc$', 'Adv', regex=True, case=False)
    return df

def shorten_class_style(df):
    df['Classes'] = df['Classes'].str.replace('^contemp$', 'Contemp', regex=True, case=False)

def remove_class_location(df):
    df['Classes'] = df['Classes'].str.replace('^live$', '', regex=True, case=False)
    df['Classes'] = df['Classes'].str.replace('^studio$', '', regex=True, case=False)
    df['Classes'] = df['Classes'].str.replace('^online', '', regex=True, case=False)
    return df

def clean_time(df):
    df['Start time'] = df['Start time'].str.rstrip('  EDT')
    return df