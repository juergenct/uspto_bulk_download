import pprint
import os
import sys
import html
import datetime

from bs4 import BeautifulSoup

utils_path = os.path.abspath('/mnt/hdd01/uspto/2023/')
sys.path.append(utils_path)

# load the psycopg to connect to postgresql
from db_interface import PGDBInterface

def print_lines(text):
    """
    Prints line by line, with the line number
    """
    count = 1
    for line in text.split("\n"):    
        print(count, line)
        count += 1    

def parse_uspto_file(bs, logging=False):
    """
    Parses a USPTO patent in a BeautifulSoup object.
    """
    
    publication_title = bs.find('invention-title').text
    publication_num = bs['file'].split("-")[0]
    publication_date = bs.find('publication-reference').find('date').text
    application_type = bs.find('application-reference')['appl-type']


    # International Patent Classification (IPC) Docs:
    # https://www.wipo.int/classifications/ipc/en/
    ipc_sections = {}
    ipc_section_classes = {}
    ipc_section_class_subclasses = {}
    ipc_section_class_subclass_groups = {}
    for classes in bs.find_all('classifications-ipcr'):
        for el in classes.find_all('classification-ipcr'):

            ipc_section = el.find('section').text
                        
            ipc_classification  = ipc_section
            ipc_classification += el.find('class').text
            ipc_classification += el.find('subclass').text
            
            ipc_group = el.find('main-group').text + "/"
            ipc_group += el.find('subgroup').text

            ipc_sections[ipc_section] = True
            ipc_section_classes[ipc_section+el.find('class').text] = True
            ipc_section_class_subclasses[ipc_classification] = True
            ipc_section_class_subclass_groups[ipc_classification+" "+ipc_group] = True
    
    # Cooperative Patent Classification (CPC) Docs:
    # https://www.cooperativepatentclassification.org/home
    main_cpc_sections = {}
    main_cpc_section_classes = {}
    main_cpc_section_class_subclasses = {}
    main_cpc_section_class_subclass_groups = {}
    further_cpc_sections = {}
    further_cpc_section_classes = {}
    further_cpc_section_class_subclasses = {}
    further_cpc_section_class_subclass_groups = {}
    for classes in bs.find_all('classifications-cpc'):
        for el in classes.find_all('main-cpc'):
            for kcp in el.find_all('classification-cpc'):
                main_cpc_section = kcp.find('section').text
                            
                main_cpc_classification  = main_cpc_section
                main_cpc_classification += kcp.find('class').text
                main_cpc_classification += kcp.find('subclass').text
                
                main_cpc_group = kcp.find('main-group').text + "/"
                main_cpc_group += kcp.find('subgroup').text

                main_cpc_sections[main_cpc_section] = True
                main_cpc_section_classes[main_cpc_section+kcp.find('class').text] = True
                main_cpc_section_class_subclasses[main_cpc_classification] = True
                main_cpc_section_class_subclass_groups[main_cpc_classification+" "+main_cpc_group] = True
        for el in classes.find_all('further-cpc'):
            for kcp in el.find_all('classification-cpc'):
                further_cpc_section = kcp.find('section').text
                        
                further_cpc_classification  = further_cpc_section
                further_cpc_classification += kcp.find('class').text
                further_cpc_classification += kcp.find('subclass').text
                
                further_cpc_group = kcp.find('main-group').text + "/"
                further_cpc_group += kcp.find('subgroup').text

                further_cpc_sections[further_cpc_section] = True
                further_cpc_section_classes[further_cpc_section+kcp.find('class').text] = True
                further_cpc_section_class_subclasses[further_cpc_classification] = True
                further_cpc_section_class_subclass_groups[further_cpc_classification+" "+further_cpc_group] = True
            
    applicants = []
    for parties in bs.find_all('us-parties'):
        for appl in parties.find_all('us-applicants'):
            for el in appl.find_all('addressbook'):
                if el.find('first-name') is not None:
                    first_name = el.find('first-name').text
                    last_name = el.find('last-name').text
                    applicants.append(first_name + " " + last_name)
                if el.find('orgname') is not None:
                    orgname = el.find('orgname').text
                    applicants.append(orgname)

    inventors = []
    for parties in bs.find_all('us-parties'):
        for inv in parties.find_all('inventors'):
            for el in inv.find_all('addressbook'):
                if el.find('first-name') is not None:
                    first_name = el.find('first-name').text
                    last_name = el.find('last-name').text
                    inventors.append(first_name + " " + last_name)
                if el.find('orgname') is not None:
                    orgname = el.find('orgname').text
                    inventors.append(orgname)
    
    assignees = []
    for parties in bs.find_all('assignees'):
        for ass in parties.find_all('assignee'):
            for el in ass.find_all('addressbook'):
                if el.find('first-name') is not None:
                    first_name = el.find('first-name').text
                    last_name = el.find('last-name').text
                    assignees.append(first_name + " " + last_name)
                if el.find('orgname') is not None:
                    orgname = el.find('orgname').text
                    assignees.append(orgname)

    pat_cit = []
    npl_cit = []
    for citations in bs.find_all('us-references-cited'):
        for ref in citations.find_all('us-citation'):
            for el in ref.find_all('patcit'):
                country = el.find('country').text
                doc_num = el.find('doc-number').text
                pat_cit.append(country + doc_num)
    
            for el in ref.find_all('nplcit'):
                othercit = el.find('othercit').text
                npl_cit.append(othercit)

    abstracts = []
    for el in bs.find_all('abstract'):
        abstracts.append(el.text.strip('\n'))
    
    descriptions = []
    for el in bs.find_all('description'):
        descriptions.append(el.text.strip('\n'))
        
    claims = []
    for el in bs.find_all('claim'):
        claims.append(el.text.strip('\n'))

    uspto_patent = {
        "publication_title": publication_title,
        "publication_number": publication_num,
        "publication_date": publication_date,
        "application_type": application_type,
        "applicants": applicants, # list
        "inventors": inventors, # list
        "assignees": assignees, # list
        "patent_citations": pat_cit, # list
        "npl_citations": npl_cit, # list
        "ipc_sections": list(ipc_sections.keys()),
        "ipc_section_classes": list(ipc_section_classes.keys()),
        "ipc_section_class_subclasses": list(ipc_section_class_subclasses.keys()),
        "ipc_section_class_subclass_groups": list(ipc_section_class_subclass_groups.keys()),
        "main_cpc_sections": list(main_cpc_sections.keys()),
        "main_cpc_section_classes": list(main_cpc_section_classes.keys()),
        "main_cpc_section_class_subclasses": list(main_cpc_section_class_subclasses.keys()),
        "main_cpc_section_class_subclass_groups": list(main_cpc_section_class_subclass_groups.keys()),
        "further_cpc_sections": list(further_cpc_sections.keys()),
        "further_cpc_section_classes": list(further_cpc_section_classes.keys()),
        "further_cpc_section_class_subclasses": list(further_cpc_section_class_subclasses.keys()),
        "further_cpc_section_class_subclass_groups": list(further_cpc_section_class_subclass_groups.keys()),
        "abstract": abstracts, # list
        "descriptions": descriptions, # list
        "claims": claims # list
    }
        
    if logging:
        
        # print(bs.prettify())
        
        print("Filename:", filename)
        print("\n\n")
        print("\n--------------------------------------------------------\n")

        print("USPTO Invention Title:", publication_title)
        print("USPTO Publication Number:", publication_num)
        print("USPTO Publication Date:", publication_date)
        print("USPTO Application Type:", application_type)
            
        count = 1
        for ipc_classification in ipc_section_class_subclass_groups:
            print("USPTO IPC Classification #"+str(count)+": " + ipc_classification)
            count += 1
        print("\n")

        count = 1
        for main_cpc_classification in main_cpc_section_class_subclass_groups:
            print("USPTO Main CPC Classification #"+str(count)+": " + main_cpc_classification)
            count += 1
        print("\n")

        count = 1
        for further_cpc_classification in further_cpc_section_class_subclass_groups:
            print("USPTO Main CPC Classification #"+str(count)+": " + further_cpc_classification)
            count += 1
        print("\n")
        
        count = 1
        for appl in applicants:
            print("Applicant #"+str(count)+": " + appl)
            count += 1
        
        count = 1
        for inventor in inventors:
            print("Inventor #"+str(count)+": " + inventor)
            count += 1

        count = 1
        for assignee in assignees:
            print("Assignee #"+str(count)+": " + assignee)
            count += 1

        count = 1
        for pat in pat_cit:
            print("Patent Citation #"+str(count)+": " + pat)
            count += 1

        count = 1
        for npl in npl_cit:
            print("Non Patent Literature Citation #"+str(count)+": " + npl)
            count += 1

        print("\n--------------------------------------------------------\n")

        print("Abstract:\n-----------------------------------------------")
        for abstract in abstracts:
            print(abstract)

        print("Description:\n-----------------------------------------------")
        for description in descriptions:
            print(description)

        print("Claims:\n-----------------------------------------------")
        for claim in claims:
            print(claim)

    title = "Shower shield system for bathroom shower drain areaways"
    if bs.find('invention-title').text == title:
        print(bs)
        exit()

            
    return uspto_patent


def write_to_db(uspto_patent, db=None):    

    """
    pp = pprint.PrettyPrinter(indent=2)
    for key in uspto_patent:
        if type(uspto_patent[key]) == list:
            if key == "ipc_section_class_subclass_groups":
                print("\n--------------------------------")
                print(uspto_patent['publication_title'])
                print(uspto_patent['publication_number'])
                print(uspto_patent['publication_date'])
                print(uspto_patent['ipc_sections'])
                print(uspto_patent['ipc_section_classes'])
                print(uspto_patent['ipc_section_class_subclasses'])
                print(uspto_patent['ipc_section_class_subclass_groups'])
                print(uspto_patent['main_cpc_sections'])
                print(uspto_patent['main_cpc_section_classes'])
                print(uspto_patent['main_cpc_section_class_subclasses'])
                print(uspto_patent['main_cpc_section_class_subclass_groups'])
                print(uspto_patent['further_cpc_sections'])
                print(uspto_patent['further_cpc_section_classes'])
                print(uspto_patent['further_cpc_section_class_subclasses'])
                print(uspto_patent['further_cpc_section_class_subclass_groups'])
                print("--------------------------------")
    """

    # Will use for created_at & updated_at time
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
    # INSERTS INTO DB
    uspto_db_entry = [
        uspto_patent['publication_title'],
        uspto_patent['publication_number'],
        uspto_patent['publication_date'],
        uspto_patent['application_type'],
        ','.join(uspto_patent['applicants']),
        ','.join(uspto_patent['inventors']),
        ','.join(uspto_patent['assignees']),
        ','.join(uspto_patent['patent_citations']),
        ','.join(uspto_patent['npl_citations']),
        ','.join(uspto_patent['ipc_sections']),
        ','.join(uspto_patent['ipc_section_classes']),
        ','.join(uspto_patent['ipc_section_class_subclasses']),
        ','.join(uspto_patent['ipc_section_class_subclass_groups']),
        ','.join(uspto_patent['main_cpc_sections']),
        ','.join(uspto_patent['main_cpc_section_classes']),
        ','.join(uspto_patent['main_cpc_section_class_subclasses']),
        ','.join(uspto_patent['main_cpc_section_class_subclass_groups']),
        ','.join(uspto_patent['further_cpc_sections']),
        ','.join(uspto_patent['further_cpc_section_classes']),
        ','.join(uspto_patent['further_cpc_section_class_subclasses']),
        ','.join(uspto_patent['further_cpc_section_class_subclass_groups']),
        '\n'.join(uspto_patent['abstract']),
        '\n'.join(uspto_patent['descriptions']),
        '\n'.join(uspto_patent['claims']),
        current_time,
        current_time
    ]

    # ON CONFLICT UPDATES TO DB
    uspto_db_entry += [
        uspto_patent['publication_title'],
        uspto_patent['publication_date'],
        uspto_patent['application_type'],
        ','.join(uspto_patent['applicants']),
        ','.join(uspto_patent['inventors']),
        ','.join(uspto_patent['assignees']),
        ','.join(uspto_patent['patent_citations']),
        ','.join(uspto_patent['npl_citations']),
        ','.join(uspto_patent['ipc_sections']),
        ','.join(uspto_patent['ipc_section_classes']),
        ','.join(uspto_patent['ipc_section_class_subclasses']),
        ','.join(uspto_patent['ipc_section_class_subclass_groups']),
        ','.join(uspto_patent['main_cpc_sections']),
        ','.join(uspto_patent['main_cpc_section_classes']),
        ','.join(uspto_patent['main_cpc_section_class_subclasses']),
        ','.join(uspto_patent['main_cpc_section_class_subclass_groups']),
        ','.join(uspto_patent['further_cpc_sections']),
        ','.join(uspto_patent['further_cpc_section_classes']),
        ','.join(uspto_patent['further_cpc_section_class_subclasses']),
        ','.join(uspto_patent['further_cpc_section_class_subclass_groups']),
        '\n'.join(uspto_patent['abstract']),
        '\n'.join(uspto_patent['descriptions']),
        '\n'.join(uspto_patent['claims']),
        current_time
    ]

    db_cursor = None
    if db is not None:
        db_cursor = db.obtain_db_cursor()
    
    if db_cursor is not None:
        db_cursor.execute("INSERT INTO uspto_patents ("
                          + "publication_title, publication_number, "
                          + "publication_date, publication_type, " 
                          + "applicants, inventors, assignees, patent_citations, npl_citations, ipc_sections, ipc_section_classes, " 
                          + "ipc_section_class_subclasses, "
                          + "ipc_section_class_subclass_groups, "
                          + "applicants, inventors, assignees, patent_citations, npl_citations, main_cpc_sections, main_cpc_section_classes, " 
                          + "main_cpc_section_class_subclasses, "
                          + "main_cpc_section_class_subclass_groups, "
                          + "applicants, inventors, assignees, patent_citations, npl_citations, further_cpc_sections, further_cpc_section_classes, " 
                          + "further_cpc_section_class_subclasses, "
                          + "further_cpc_section_class_subclass_groups, "
                          + "abstract, description, claims, "
                          + "created_at, updated_at"
                          + ") VALUES ("
                          + "%s, %s, %s, %s, %s, %s, %s, %s, "
                          + "%s, %s, %s, %s, %s, %s) "
                          + "ON CONFLICT(publication_number) "
                          + "DO UPDATE SET "
                          + "publication_title=%s, "
                          + "publication_date=%s, "
                          + "publication_type=%s, "
                          + "applicants=%s, "
                          + "inventors=%s, "
                          + "assignees=%s, "
                          + "patent_citations=%s, "
                          + "npl_citations=%s, "
                          + "ipc_sections=%s, ipc_section_classes=%s, "
                          + "ipc_section_class_subclasses=%s, "
                          + "ipc_section_class_subclass_groups=%s, "
                          + "main_cpc_sections=%s, main_cpc_section_classes=%s, "
                          + "main_cpc_section_class_subclasses=%s, "
                          + "main_cpc_section_class_subclass_groups=%s, "
                          + "further_cpc_sections=%s, further_cpc_section_classes=%s, "
                          + "further_cpc_section_class_subclasses=%s, "
                          + "further_cpc_section_class_subclass_groups=%s, "
                          + "abstract=%s, description=%s, "
                          + "claims=%s, updated_at=%s", uspto_db_entry)

    return 
    

arg_filenames = ['/mnt/hdd01/uspto/2023/test2023.xml']
if len(sys.argv) > 1:
    arg_filenames = sys.argv[1:]

filenames = []
for filename in arg_filenames:
    # Load listed directories
    if os.path.isdir(filename):
        print("directory", filename)
        for dir_filename in os.listdir(filename):
            directory = filename
            if directory[-1] != "/":
                directory += "/"
            filenames.append(directory + dir_filename)                
                
    # Load listed files
    if ".xml" in filename:
        filenames.append(filename)

print("LOADING FILES TO PARSE\n----------------------------")
for filename in filenames:
    print(filename)

db_config_file = "config/postgres.tsv"
db = PGDBInterface(config_file=db_config_file)
db.silent_logging = True
    
count = 1
success_count = 0
errors = []
for filename in filenames:
    if ".xml" in filename:
        
        xml_text = html.unescape(open(filename, 'r').read())
        
        for patent in xml_text.split("<?xml version=\"1.0\" encoding=\"UTF-8\"?>"):

            if patent is None or patent == "":
                continue
    
            bs = BeautifulSoup(patent)

            if bs.find('sequence-cwu') is not None:
                continue # Skip DNA sequence documents
    
            application = bs.find('us-patent-application')
            if application is None: # If no application, search for grant
                application = bs.find('us-patent-grant')
            title = "None"
    
            try:
                title = application.find('invention-title').text
            except Exception as e:          
                print("Error", count, e)

            try:
                uspto_patent = parse_uspto_file(application)
                write_to_db(uspto_patent, db=db)
                success_count += 1
            except Exception as e:
                exception_tuple = (count, title, e)
                errors.append(exception_tuple)
                print(exception_tuple)
       
            if (success_count+len(errors)) % 50 == 0:
                print(count, filename, title)
                db.commit_to_db()
            count += 1
            os._exit(1)


print("\n\nErrors\n------------------------\n")
for e in errors:
    print(e)
    
print("Success Count:", success_count)
print("Error Count:", len(errors))
