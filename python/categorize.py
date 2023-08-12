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

#
is_theater = ['theater','broadway']
is_tap = ['tap']
is_ballet = ['ballet', 'pointe','barre']
is_contemporary_modern = ['contemp','modern','horton','graham','dunham','limón','cunningham','gaga']
is_street = ['hip hop', 'hip-hop', 'tutting', 'heels', 'styling free','stilettos',
             'popping','breaking','jerz','locking','house','street','urban',
             'chairography','vogue','choreo','pop up','funk','wacking','waacking'
             'comm','grooves','fusion','beg waacking']
is_jazz = ['jazz']
is_world = ['salsa', 'afro', 'african', 'dancehall', 'reggaeton', 'congolese', 
            'sabar', 'haitian','mambo']

all_styles = [is_theater, is_tap, is_ballet, is_contemporary_modern, is_street, is_jazz, is_world]

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

        # skip rehearsals
        if class_name == 'private rehearsal': continue

        for style in all_styles:
            if style_found: continue        # skip if found
            for name in style:
                if style_found: continue    # skip if found
                if name in class_name:
                    # add the row to the correct list
                    if (style == all_styles[0]):
                        theater.append(row[1])
                    elif (style == all_styles[1]):
                        tap.append(row[1])
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

street_df.to_csv(f'{styles_path}/street_styles_choreography.csv', index=False, header=False)
ballet_df.to_csv(f'{styles_path}/ballet.csv', index=False, header=False)
contemporary_modern_df.to_csv(f'{styles_path}/contemporary_modern.csv', index=False, header=False)
jazz_df.to_csv(f'{styles_path}/jazz.csv', index=False, header=False)
tap_df.to_csv(f'{styles_path}/tap.csv', index=False, header=False)
theater_df.to_csv(f'{styles_path}/theater.csv', index=False, header=False)
world_df.to_csv(f'{styles_path}/world.csv', index=False, header=False)
other_df.to_csv(f'{styles_path}/additional_disciplines.csv', index=False, header=False)