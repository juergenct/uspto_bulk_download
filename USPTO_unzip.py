import os
from termcolor import colored
from tqdm import tqdm
import multiprocessing as mp

# Loop through the years and unzip the data for each year
# for year in years:
def process_year(year):
    print(colored('Starting to unzip USPTO dataset year: %d' % year, 'green'))
    
    # Get a list of all the zip files in the current year's directory
    zip_directory = f"/mnt/hdd01/uspto/{year}"
    target_directory = f"/mnt/hdd01/uspto/xml/{year}"
    zip_files = [f for f in os.listdir(zip_directory) if f.endswith('.zip')]

    # Unzip each zip file
    for zip_file in tqdm(zip_files):
        # Create the target directory if it doesn't exist
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        # Unzip the file
        os.system(f"unzip -o {zip_directory}/{zip_file} -d {target_directory}/{zip_file}")
        # Throw away the zip file
        # os.system(f"rm {directory}/{zip_file}")

if __name__ == '__main__':
    # Specify the years for which you want to unzip the data
    years = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

    num_CPUs = mp.cpu_count() - 4
    pool = mp.Pool(processes=num_CPUs)
    pool.map(process_year, years)
    pool.close()
    pool.join()