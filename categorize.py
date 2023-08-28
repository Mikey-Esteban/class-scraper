import os
import pandas as pd
from tabulate import tabulate
from helpers import *
from df_helpers import *

test_path = f'./csv/22_03_2023/social'
test_styles_path = f'./csv/22_03_2023/styles'

path = f'./csv/{get_date()}/social'
styles_path = f'./csv/{get_date()}/styles'
files = os.listdir(path)

if not os.path.exists(styles_path):
    os.makedirs(styles_path)

street_styles_choreography = []
ballet = []
contemporary_modern = []
jazz = []
tap = []
theater = []
world_dance = []
other = []

# categorization logic
is_tap = ['tap']
is_theater = ['theater','broadway']
is_ballet = ['ballet','pointe','barre','ballez']
is_contemporary_modern = ['contemp','modern','horton','graham','dunham','limón','cunningham','gaga', 'lyrical']
is_street = ['hip hop', 'hip-hop', 'tutting', 'heels', 'styling free','stilettos',
             'popping','breaking','jerz','locking','house','street','urban',
             'chairography','vogue','choreo','pop up','funk','wacking','waacking',
             'grooves','fusion','hustle','breakin','modega','voguing', 'litefeet', 'expressive', 'krump', 'shapes', 'master', 'battle', 'jen bayan', 'pop-up']
is_jazz = ['jazz']
is_world = ['salsa', 'afro', 'african', 'dancehall', 'reggaeton', 'congolese', 
            'sabar', 'haitian','mambo', 'samba', 'bhangra', 'capoeira','latin','guinean', 'indian', 'flamenco']

all_styles = [is_tap, is_theater, is_ballet, is_contemporary_modern, is_street, is_jazz, is_world]


for f in files:
    print(f)

    df = pd.read_csv(f'{path}/{f}', index_col=False)

    for row in df.iterrows():
        # fast track ATDF
        studio = row[1][0].lower()
        if studio == 'atdf':
            tap.append(row[1])
            continue

        class_name = row[1][2].lower()
        style_found = False

        # trash / skipped classes
        if 'private' in class_name or 'rehearsal' in class_name or 'auditions' in class_name:
            continue

        for style in all_styles:
            if style_found: continue        # skip if found
            for name in style:
                if style_found: continue    # skip if found
                if name in class_name:
                    # add the row to the correct list
                    if (style == all_styles[0]):
                        tap.append(row[1])
                    elif (style == all_styles[1]):
                        theater.append(row[1])
                    elif (style == all_styles[2]):
                        ballet.append(row[1])
                    elif (style == all_styles[3]):
                        contemporary_modern.append(row[1])
                    elif (style == all_styles[4]):
                        street_styles_choreography.append(row[1])
                    elif (style == all_styles[5]):
                        jazz.append(row[1])
                    elif (style == all_styles[6]):
                        world_dance.append(row[1])
                    style_found = True
                
        if not style_found:
            print('did not find style', class_name)
            other.append(row[1])

    print()
    print()
# print('hip hop')
# for el in street_styles_choreography:
#     print(tabulate(el[1]))

street_df = pd.DataFrame(street_styles_choreography)
ballet_df = pd.DataFrame(ballet)
contemporary_modern_df = pd.DataFrame(contemporary_modern)
jazz_df = pd.DataFrame(jazz)
tap_df = pd.DataFrame(tap)
theater_df = pd.DataFrame(theater)
world_df = pd.DataFrame(world_dance)
other_df = pd.DataFrame(other)

rename_columns_output(street_df)
rename_columns_output(ballet_df)
rename_columns_output(contemporary_modern_df)
rename_columns_output(jazz_df)
rename_columns_output(tap_df)
rename_columns_output(theater_df)
rename_columns_output(world_df)
rename_columns_output(other_df)

street_df['Date'] = pd.Timestamp(f'{get_date2()}')
ballet_df['Date'] = pd.Timestamp(f'{get_date2()}')
contemporary_modern_df['Date'] = pd.Timestamp(f'{get_date2()}')
jazz_df['Date'] = pd.Timestamp(f'{get_date2()}')
tap_df['Date'] = pd.Timestamp(f'{get_date2()}')
theater_df['Date'] = pd.Timestamp(f'{get_date2()}')
world_df['Date'] = pd.Timestamp(f'{get_date2()}')
other_df['Date'] = pd.Timestamp(f'{get_date2()}')

street_df['Style'] = 'Street/Choreography'
ballet_df['Style'] = 'Ballet'
contemporary_modern_df['Style'] = 'Contemporary/Modern'
jazz_df['Style'] = 'Jazz'
tap_df['Style'] = 'Tap'
theater_df['Style'] = 'Theater'
world_df['Style'] = 'World'
other_df['Style'] = 'Additional Disciplines'

all_df = pd.concat([street_df,ballet_df,contemporary_modern_df,jazz_df,tap_df,theater_df,world_df,other_df])

all_df.sort_values(by='Time', inplace=True)
street_df.sort_values(by='Time', inplace=True)
ballet_df.sort_values(by='Time', inplace=True)
contemporary_modern_df.sort_values(by='Time', inplace=True)
jazz_df.sort_values(by='Time', inplace=True)
tap_df.sort_values(by='Time', inplace=True)
theater_df.sort_values(by='Time', inplace=True)
world_df.sort_values(by='Time', inplace=True)
other_df.sort_values(by='Time', inplace=True)

all_df.to_csv(f'{styles_path}/all.csv', index=False, header=True)
street_df.to_csv(f'{styles_path}/street_styles_choreography.csv', index=False, header=False)
ballet_df.to_csv(f'{styles_path}/ballet.csv', index=False, header=False)
contemporary_modern_df.to_csv(f'{styles_path}/contemporary_modern.csv', index=False, header=False)
jazz_df.to_csv(f'{styles_path}/jazz.csv', index=False, header=False)
tap_df.to_csv(f'{styles_path}/tap.csv', index=False, header=False)
theater_df.to_csv(f'{styles_path}/theater.csv', index=False, header=False)
world_df.to_csv(f'{styles_path}/world.csv', index=False, header=False)
other_df.to_csv(f'{styles_path}/additional_disciplines.csv', index=False, header=False)