# to handle  data retrieval
import requests
# to handle certificate verification
import certifi
# to manage json data
import json
# for pandas dataframes
import pandas as pd
import datetime as dt
import ipywidgets as widgets
import os

__author__ = 'Mark Chua'
__credits__ = ['Mark Chua', 'Sebastian Echeverry', 'Giada Innocenti']
__version__ = '1.0.0'
__maintainer__ = 'Mark Chua'
__email__ = 'mchua004@gmail.com'
__status__ = 'Development'

output_file = 'covid_data/data.csv'

# return the covid data as a pandas dataframe
def get_covid_data():
    # URL for GET requests to retrieve vehicle data
    url = 'https://covidtracking.com/api/states/daily'

    # Perform a get request for this character
    response = requests.get(url)

    # Storing the JSON response within a variable
    data = response.json()

    # in this dataset, the data to extract is under 'features'
    covidtracking_df = pd.json_normalize(data)

    # export dataframe to a csv file
    data_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(data_path, output_file)
    covidtracking_df.to_csv(data_path, index = False, header=True)

    # send off the data to whomever called me!
    return covidtracking_df



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

valid_states = [
    'Alabama',
    'Alaska',
    'Arizona',
    'Arkansas',
    'California',
    'Colorado',
    'Connecticut',
    'Delaware',
    'Florida',
    'Georgia',
    'Hawaii',
    'Idaho',
    'Illinois',
    'Indiana',
    'Iowa',
    'Kansas',
    'Kentucky',
    'Louisiana',
    'Maine',
    'Maryland',
    'Massachusetts',
    'Michigan',
    'Minnesota',
    'Mississippi',
    'Missouri',
    'Montana',
    'Nebraska',
    'Nevada',
    'New Hampshire',
    'New Jersey',
    'New Mexico',
    'New York',
    'North Carolina',
    'North Dakota',
    'Ohio',
    'Oklahoma',
    'Oregon',
    'Pennsylvania',
    'Pennsylvannia',
    'Rhode Island',
    'South Carolina',
    'South Dakota',
    'Tennessee',
    'Texas',
    'Utah',
    'Vermont',
    'Virginia',
    'Washington',
    'West Virginia',
    'Wisconsin',
    'Wyoming',
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
    'US Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

def get_data(date_min=None, date_max=None, exclude_states=True):
    '''
    '''
    raw_data = pd.DataFrame()    
    try: raw_data = get_covid_data()
    except:
        print(f'\tERROR loading data from file at {output_file}')
        data_path = os.path.dirname(os.path.realpath(__file__))
        data_path = os.path.join(data_path, output_file)
        raw_data = pd.read_csv(data_path)
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
    # remove excluded states
    if exclude_states:
        raw_data = raw_data[raw_data['state'].isin(valid_states)]
        raw_data.reset_index(drop=True, inplace=True) 
    # send off with headers and 
    return raw_data[covid_headers + [positiveTests]].fillna(0.)
