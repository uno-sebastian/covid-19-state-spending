import json
import pandas as pd
import datetime as dt
import json
import ipywidgets as widgets
import df_function

covid_headers = [
    'date',
    'state',
    'positive', 
    'negative', 
    'onVentilatorCumulative', 
    'recovered', 
    'death', 
    'hospitalized'
]

extra_positive_headers = [
    'positiveTestsViral',
    'positiveTestsAntibody',
    'positiveTestsPeopleAntibody',
    'positiveTestsPeopleAntigen',
    'positiveTestsAntigen'
]

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

def get_data(date_min=None, date_max=None):
    '''
    '''
    raw_data = pd.DataFrame()    
    try: raw_data = df_function.get_covid_data()
    except:
        print(f'\tERROR loading data from file at {output_file}')
        raw_data = pd.read_csv(output_file)
    raw_data['date'] = pd.to_datetime(raw_data['date'], format='%Y%m%d')
    # filter with date min
    if date_min:
        raw_data = raw_data[raw_data['date'] >= date_min]
    # filter with date max
    if date_max:
        raw_data = raw_data[raw_data['date'] <= date_max]
    # add positiveTests
    positiveTests = 'positiveTests'
    raw_data[positiveTests] = pd.Series([0 for i in range(raw_data.shape[0])])
    for index, row in raw_data.iterrows():
        posTests = row[extra_positive_headers].sum()
        raw_data.at[index, positiveTests] = posTests
    abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))
    # convert states
    for index, row in raw_data.iterrows():
        raw_data.at[index, 'state'] = abbrev_us_state[row['state']]
    # send off with headers and 
    return raw_data[covid_headers + [positiveTests]].dropna()