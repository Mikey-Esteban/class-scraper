from even_odd_rows import *
from full_week import *

#     {'name': 'aileystudios', 'id':'851', 'tab_ids': ['tabA111', 'tabA10'], 'func': run_even_odds_csv, 'filenames': ['ailey_online.csv', 'ailey_in_person.csv']},
#     {'name': 'atdf', 'id':'14721', 'tab_ids': ['tabA118'], 'func': run_full_week_csv, 'date_format': '%A %B %d, %Y', 'filenames': ['atdf.csv']},
#     {'name': 'balletacademyeast', 'id': '30500', 'tab_ids': ['tabA7'], 'func': run_full_week_csv, 'date_format': '%A %B %d, %Y', 'filenames': ['ballet_academy_east.csv']},
#     {'name': 'balletarts', 'id': '589886', 'tab_ids': ['tabA7'], 'func': run_even_odds_csv, 'filenames': ['ballet_arts.csv']},
#     {'name': 'broadwaydancecenter', 'id': '28329', 'tab_ids': ['tabA7'], 'func': run_even_odds_csv, 'filenames': ['bdc.csv']},
#     {'name': 'brickhouse', 'id': '807568', 'tab_ids': ['tabA7'], 'func': run_full_week_csv, 'date_format': '%A %B %d, %Y', 'filenames': ['brickhouse.csv']},
#     {'name': 'cumbe', 'id': '16827', 'tab_ids': ['tabA112', 'tabA111'], 'func': run_full_week_csv, 'date_format': '%a %B %d, %Y', 'filenames': ['cumbe_in_person.csv', 'cumbe_online.csv']},
#     {'name': 'gibney', 'id': '31459', 'tab_ids': ['tabA7'], 'func': run_full_week_csv, 'date_format': '%a %B %d, %Y', 'filenames': ['gibney.csv']},
#     {'name': 'ild', 'id': '144750', 'tab_ids': ['tabA104', 'tabA103', 'tabA102', 'tabA105'], 'func': run_full_week_csv, 'date_format': '%a %B %d, %Y', 'filenames': ['ild_manhattan.csv', 'ild_nj.csv', 'ild_queens.csv', 'ild_online.csv' ]},
#     {'name': 'markmorris', 'id': '95201', 'tab_ids': ['tabA7'], 'func': run_full_week_csv, 'date_format': '%a %B %d, %Y', 'filenames': ['mark_morris.csv']},
    # {'name': 'peridance', 'id': '38909', 'tab_ids': ['tabA125', 'tabA126'], 'func': run_full_week_csv, 'date_format': '%a %B %d, %Y', 'filenames': ['peridance_in_person.csv', 'peridance_online.csv']},
    # {'name': 'pmt', 'id': '727061', 'tab_ids': ['tabA7'], 'func': run_full_week_csv, 'date_format': '%A %B %d, %Y', 'filenames': ['pmt.csv']},
    # {'name': 'sass', 'id': '988409', 'tab_ids': ['tabA103', 'tabA106'], 'func': run_full_week_csv, 'date_format': '%a %B %d, %Y', 'filenames': ['sass_in_person.csv', 'sass_online.csv']},
    # {'name': 'steps', 'id': '-308', 'tab_ids': ['tabA107', 'tabA109'], 'func': run_full_week_csv, 'date_format': '%A %B %d, %Y', 'filenames': ['steps_in_person.csv', 'steps_online.csv']},
    # {'name': 'taylor', 'id': '463013', 'tab_ids': ['tabA7'], 'func': run_full_week_csv, 'date_format': '%A %B %d, %Y', 'filenames': ['taylor.csv']},

studios = [
    {
        'name': 'aileystudios', 
        'id':'851', 
        'tab_ids': ['tabA10','tabA111'], 
        'func': run_even_odds_csv, 
        'filenames': ['ailey.csv', 'ailey.csv']
    },
    {
        'name': 'atdf', 
        'id':'14721', 
        'tab_ids': ['tabA118'], 
        'func': run_full_week_csv, 
        'date_format': '%a %B %d, %Y', 
        'filenames': ['atdf.csv']
    },
    {
        'name': 'balletacademyeast', 
        'id': '30500', 
        'tab_ids': ['tabA7'], 
        'func': run_full_week_csv, 
        'date_format': '%A %B %d, %Y', 
        'filenames': ['ballet_academy_east.csv']
    },
    {
        'name': 'balletarts', 
        'id': '589886', 
        'tab_ids': ['tabA7'], 
        'func': run_even_odds_csv, 
        'filenames': ['ballet_arts.csv']
    },
    {
        'name': 'broadwaydancecenter', 
        'id': '28329', 
        'tab_ids': ['tabA7'], 
        'func': run_even_odds_csv, 
        'filenames': ['bdc.csv']
    },
    {
        'name': 'brickhouse', 
        'id': '807568', 
        'tab_ids': ['tabA7'], 
        'func': run_full_week_csv, 
        'date_format': '%A %B %d, %Y', 
        'filenames': ['brickhouse.csv']
    },
    {
        'name': 'cumbe', 
        'id': '16827', 
        'tab_ids': ['tabA112', 'tabA111'], 
        'func': run_full_week_csv, 
        'date_format': '%a %B %d, %Y', 
        'filenames': ['cumbe.csv', 'cumbe.csv']
    },
    {
        'name': 'gibney', 
        'id': '31459', 
        'tab_ids': ['tabA7'], 
        'func': run_full_week_csv, 
        'date_format': '%a %B %d, %Y', 
        'filenames': ['gibney.csv']
    },
    {
        'name': 'ild', 
        'id': '144750', 
        'tab_ids': ['tabA104', 'tabA103', 'tabA102', 'tabA105'],
        'func': run_full_week_csv, 
        'date_format': '%a %B %d, %Y', 
        'filenames': ['ild_manhattan.csv', 'ild_nj.csv', 'ild_queens.csv', 'ild_online.csv' ]
    },
    {
        'name': 'markmorris', 
        'id': '95201', 
        'tab_ids': ['tabA7'], 
        'func': run_full_week_csv, 
        'date_format': '%a %B %d, %Y', 
        'filenames': ['mark_morris.csv']
    },
    {
        'name': 'peridance', 
        'id': '38909', 
        'tab_ids': ['tabA125'], 
        'func': run_full_week_csv, 
        'date_format': '%a %B %d, %Y', 
        'filenames': ['peridance.csv']
    },
    {
        'name': 'pmt', 
        'id': '727061', 
        'tab_ids': ['tabA7'], 
        'func': run_full_week_csv, 
        'date_format': '%A %B %d, %Y', 
        'filenames': ['pmt.csv']
    },
    {
        'name': 'sass', 
        'id': '988409', 
        'tab_ids': ['tabA103', 'tabA106'], 
        'func': run_full_week_csv, 
        'date_format': '%a %B %d, %Y', 
        'filenames': ['sass.csv', 'sass.csv']
    },
    {
        'name': 'steps', 
        'id': '-308', 
        'tab_ids': ['tabA107', 'tabA109'], 
        'func': run_full_week_csv, 
        'date_format': '%A %B %d, %Y', 
        'filenames': ['steps.csv', 'steps.csv']
    },
    {
        'name': 'taylor', 
        'id': '463013', 
        'tab_ids': ['tabA7'], 
        'func': run_full_week_csv, 
        'date_format': '%a %B %d, %Y', 
        'filenames': ['taylor.csv']
    },
]
