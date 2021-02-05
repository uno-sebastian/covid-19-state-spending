# to handle  data retrieval
import requests
# to handle certificate verification
import certifi
# to manage json data
import json
# for pandas dataframes
import pandas as pd

__author__ = 'Mark Chua'
__credits__ = ['Mark Chua']
__version__ = '1.0.0'
__maintainer__ = 'Mark Chua'
__email__ = 'mchua004@gmail.com'
__status__ = 'Development'

# return the covid data as a pandas dataframe
def get_covid_data(input):
    # URL for GET requests to retrieve vehicle data
    url = 'https://covidtracking.com/api/states/daily'

    # Perform a get request for this character
    response = requests.get(url)

    # Storing the JSON response within a variable
    data = response.json()

    # in this dataset, the data to extract is under 'features'
    covidtracking_df = pd.json_normalize(data)

    # export dataframe to a csv file
    covidtracking_df.to_csv (r'covidtracking_dataframe.csv', index = False, header=True)

    # send off the data to whomever called me!
    return covidtracking_df
