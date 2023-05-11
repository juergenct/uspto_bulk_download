import os
from termcolor import colored
from tqdm import tqdm
import multiprocessing as mp

# Specify the years for which you want to download data
years = [2007, 2010] 

# Loop through the years and download the data for each year
# for year in years:
def process_year(year):
    print(colored('Starting to download USPTO dataset year: %d' % year, 'green'))
    
    # Specify the base URL for the USPTO patent data website
    base_url = "https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext"

    # Specify the URL for the data of the current year
    url = f"{base_url}/{year}/"
    
    # Create a directory for the current year's data
    directory = f"/mnt/hdd01/uspto/{year}"
    os.makedirs(directory, exist_ok=True)
    # directory = f"/mnt/hdd01/uspto"

    # Download the data for the current year
    os.system(f"wget -r -np -l1 -nd -A zip {url} -P {directory}")

if __name__ == '__main__':
    num_CPUs = mp.cpu_count() - 4
    pool = mp.Pool(processes=num_CPUs)
    pool.map(process_year, years)
    pool.close()
    pool.join()