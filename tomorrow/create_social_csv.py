import os
import pandas as pd
from helpers import *
from df_helpers import *

test_path = f'./csv/22_03_2023/live'
test_w_path = f'./csv/22_03_2023/social'

path = f'./csv/{get_date()}/live'
w_path = f'./csv/{get_date()}/social'
files = os.listdir(path)

for f in files:
    print(f)

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