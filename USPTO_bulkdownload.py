import os
from termcolor import colored
from tqdm import tqdm

# Specify the years for which you want to download data
years = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023] 

# Specify the base URL for the USPTO patent data website
base_url = "https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext"

# Loop through the years and download the data for each year
for year in years:
    print(colored('Starting to download USPTO dataset year: %d' % year, 'green'))
    
    # Specify the URL for the data of the current year
    url = f"{base_url}/{year}/"
    
    # Create a directory for the current year's data
    directory = f"/mnt/hdd01/uspto/{year}"
    os.makedirs(directory, exist_ok=True)
    # directory = f"/mnt/hdd01/uspto"

    # Download the data for the current year
    os.system(f"wget -r -np -l1 -nd -A zip {url} -P {directory}")

