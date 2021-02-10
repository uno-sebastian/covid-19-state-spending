import os
import json
import ipywidgets as widgets
import time
import pandas as pd

out = widgets.Output(layout={'border': '1px solid black'})

crfb_files = {
    '2021-02-09' : '20210209_cmt.xlsx',
    '2021-02-08' : '20210208_alt_cmt.xlsx',
    '2021-02-03' : '20210203_cmt.csv',
    '2021-02-02' : '20210202_new_alternative_cmt.xlsx',
    '2021-01-25' : '20210125_cmt.xlsx',
    '2021-01-20' : '20210120_cmt.xlsx',
    '2020-12-21' : '12212020_cmt.xlsx',
    '2020-12-14' : '12142020_new_cmt.xlsx',
    '2020-12-07' : '12072020_new_cmt.xlsx',
    '2020-11-30' : '11302020_new_cmt.xlsx',
    '2020-11-20' : '11202020_cmt.xlsx',
    '2020-11-13' : '11132020_cmt.xlsx',
    '2020-11-09' : '11092020_cmt.xlsx',
    '2020-10-30' : '10302020_cmt.xlsx',
    '2020-10-28' : '10282020_cmt.xlsx',
    '2020-10-23' : 'cmt_main_10232020.xlsx'
}

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

crfb_headers = [
    'Recipient State',
    'Amount Committed/Disbursed',
    'Date',
    'Recipient Type',
    'Legislation',
    'Agency'
]

# get the multi values indexes in the serise column
def get_multi_values_indexs(column):
    mulit_values = []
    for index, value in column.items():
        if ';' in str(value):
            mulit_values.append(index)
    return mulit_values

def split_mulit_states(compressed_data, exclude_states):
    uncompressed = pd.DataFrame()
    for index, row in compressed_data.iterrows():
        split_names = fr'{row["Recipient State"]}'.split(';')
        row['Amount Committed/Disbursed'] = row['Amount Committed/Disbursed'] / len(split_names)
        for state_name in split_names:
            if exclude_states and state_name not in valid_states:
                continue
            new_row = pd.DataFrame([row])
            new_row['Recipient State'] = state_name
            uncompressed = pd.concat([uncompressed, new_row])
    return uncompressed

def clean_raw_crfb_data(raw_data, exclude_states):
    """
    clean the raw crfb data by removing nulls in ['Date', 
    'Amount Committed/Disbursed', 'Recipient State'] and
    spliting the multi states values amongst the 'Amount Committed/Disbursed'    
    
    Parameters
    ----------
        raw_data — RAW data from either csv or xlsx
        exclude_states — Exclude any state outside the common 50 known
    """
    data = pd.DataFrame(raw_data[crfb_headers])
    # drop null values for 'Date', 'Amount Committed/Disbursed', 'Recipient State'
    data.dropna(subset=['Date', 'Amount Committed/Disbursed', 'Recipient State'], inplace=True)
    data.reset_index(drop=True, inplace=True)
    # format money
    data['Amount Committed/Disbursed'] = data['Amount Committed/Disbursed'].replace('[\$,]', '', regex=True).astype(float)
    # format date
    data['Date']= pd.to_datetime(data['Date'], format='%m/%d/%Y')
    # find and seperate multi states
    mulit_states = get_multi_values_indexs(data['Recipient State'])
    if len(mulit_states) > 0:
        states = split_mulit_states(pd.DataFrame(data.iloc[mulit_states,:]), exclude_states)
        data.drop(mulit_states, inplace=True)
        data.reset_index(drop=True, inplace=True)
        if states.shape[0] > 0:
            data = pd.concat([data, states])
    return data.reset_index(drop=True)

def get_data_date(date, exclude_states=True):
    """
    Get the data from the Committee for a Responsible Federal Budget 
    
    Parameters
    ----------
        exclude_states — Exclude any state outside the common 50 known
    """
    data_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(data_path, 'crfb_raw_data')
    # create temp var to hold our data
    df = pd.DataFrame()
    if date not in crfb_files:
        print(f'there is no file for date {date}')
        return df
    print(f'loading data from date {date} : file {crfb_files[date]}...')
    path = os.path.join(data_path, crfb_files[date])
    try:
        df = pd.DataFrame()
        if path.endswith('.csv'): df = pd.read_csv(path)
        else: df = pd.read_excel(path, index_col=0)
        df = clean_raw_crfb_data(df, exclude_states)
    except Exception as e:
        print(f'failed to load data {path}\nERROR: {e}')
    return df

def get_data_single(index=0, exclude_states=True):
    """
    Get the data from the Committee for a Responsible Federal Budget 
    
    Parameters
    ----------
        exclude_states — Exclude any state outside the common 50 known
    """
    date = [key for key in crfb_files.keys()][index]
    return get_data_date(date, exclude_states)

def get_data_all(exclude_states=True):
    """
    Get the data from the Committee for a Responsible Federal Budget 
    
    Parameters
    ----------
        exclude_states — Exclude any state outside the common 50 known
    """
    # create temp var to hold our data
    crfb_data = pd.DataFrame()
    for key, value in crfb_files.items():
        df = get_data_date(key, exclude_states)
        if df.shape[0] > 0:
            re_order = ['Date CRFB Downloaded'] + list(df.columns)
            write_date = pd.Series([key for i in range(len(df['Amount Committed/Disbursed']))])
            df[re_order[0]] = pd.to_datetime(write_date, format='%Y-%m-%d')
            crfb_data = pd.concat([crfb_data, df.reindex(columns=re_order)])
        else:
            parsed = json.loads(df.to_json())
            print(f'failed to concat dataframe of value\n{json.dumps(parsed, indent=4) }')
    out.clear_output()
    return crfb_data
