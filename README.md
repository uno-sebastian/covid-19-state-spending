# Control-Alt-Elite

## Dataset

Found dataset at https://www.usaspending.gov/download_center/custom_account_data

Used COVID's Disaster Fund Emergency codes in the filters to get all records from the Health budget. 

Printed out dataframes in jupyter notebook. Time for cleaning!

Added covid_frame with "national_interest_action" == "COVID 19 2020"

---------------------------------------------------------------------------------------------

## Dataset Summaries

First dataset: Budget account balnces. going to need to merge with covid frame to get prices amount spent. I have some research about how the data works.

    - Contract vs. Grant 
    -- Grants are a form of financial assistance
    -- Contracts are for when the government needs to purchase something big at a certain time.  
    --- LOOKING FOR GRANTS ONLY 

    - Outlay vs. Obligation
    -- Outlay is when fundas are actually spent
    -- Obligation is a promise to pay 
    --- Outlays should be the main focus for analysis

Second dataset: The meat and potatoes, the who gets what, the transaction records. This is where covid data is pulled from and gives us some geographic location. A creation of a reference file could match places to lat and long. Maybe there is a way to use google api? 

Third dataset: Gives counts of how many times they had to promise money to each account? May have to dig deeper on this one. 
