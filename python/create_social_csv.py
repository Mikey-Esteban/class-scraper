import os
import pandas as pd
from helpers import *
from df_helpers import *

path = f'./csv/{get_date()}/live'
w_path = f'./csv/{get_date()}/social'
files = os.listdir(path)

for f in files:
    print(f)

    df = pd.read_csv(f'{path}/{f}', index_col=False)


    strip_time(df)
    rename_columns(df)
    remove_colon_from_class(df)
    remove_brackets_from_class(df)
    remove_brackets_from_class(df)
    remove_type_from_instructor(df)
    shorten_class_level(df)
    remove_instructor_from_class(df)
    shorten_class_style(df)
    titleize_classes(df, 'Classes')

    df = df.dropna()
    df.to_csv(f'{w_path}/{f}', index=False)