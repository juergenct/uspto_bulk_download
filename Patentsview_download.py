import os
from tqdm import tqdm
import multiprocessing as mp

# Specify the links which you want to download data
links = ['https://s3.amazonaws.com/data.patentsview.org/download/g_applicant_not_disambiguated.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_application.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_assignee_disambiguated.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_assignee_not_disambiguated.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_attorney_disambiguated.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_attorney_not_disambiguated.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_botanic.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_cpc_current.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_cpc_title.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_examiner_not_disambiguated.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_figures.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_foreign_citation.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_foreign_priority.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_gov_interest.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_gov_interest_contracts.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_gov_interest_org.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_inventor_disambiguated.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_inventor_not_disambiguated.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_ipc_at_issue.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_location_disambiguated.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_location_not_disambiguated.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_other_reference.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_patent.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_pct_data.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_persistent_assignee.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_persistent_inventor.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_rel_app_text.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_uspc_at_issue.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_us_application_citation.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_us_patent_citation.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_us_rel_doc.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_us_term_of_grant.tsv.zip',
'https://s3.amazonaws.com/data.patentsview.org/download/g_wipo_technology.tsv.zip'] 

# Loop through the links
def process_link(link):
        
    directory = f"/mnt//hdd01/patentsview"

    # Download the data for the current year
    os.system(f"wget -r -np -l1 -nd -A zip {link} -P {directory}")

if __name__ == '__main__':
    num_CPUs = mp.cpu_count() - 4
    pool = mp.Pool(processes=num_CPUs)
    pool.map(process_link, links)
    pool.close()
    pool.join()