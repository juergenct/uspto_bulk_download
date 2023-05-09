import os
from termcolor import colored
from tqdm import tqdm

# Specify the years for which you want to download data
years = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

# Loop through the years and unzip the data for each year
for year in years:
    print(colored('Starting to unzip USPTO dataset year: %d' % year, 'green'))
    
    # Get a list of all the zip files in the current year's directory
    directory = f"/mnt/hdd01/uspto/{year}"
    zip_files = [f for f in os.listdir(directory) if f.endswith('.zip')]

    # Unzip each zip file
    for zip_file in tqdm(zip_files):
        os.system(f"unzip -o {directory}/{zip_file} -d {directory}")
        # Throw away the zip file
        os.system(f"rm {directory}/{zip_file}")