from CVdjango.base.db.utils import *
from CVdjango.base.scrapers.researchgate_scraper import *
from CVdjango.base.scrapers.google_search import *
from CVdjango.base.scrapers.researchgate import *
from CVdjango.base.scrapers.scholar import *
from CVdjango.base.scrapers.scholar_api import *


mongo_handler = MongoDBHandler("localhost", 27017)
client = mongo_handler.connect()
# TODO SOS
author = 'Serafeim Moustakidis'

if client:
    db, col = mongo_handler.get_database_and_collection('CVproject', 'Candinates')
    # TODO Find
    # check which url is empty
    # if it is empty then we have to run it
    # TODO Insert after the PDF

    # ok = mongo_handler.insert_one_document(col)
    profile = mongo_handler.find_document_one(col, author)

    if profile:
        print(f"The query returned some Documents for the Candidate '{profile['author']}'.")
        #Update Candidate researchGate profile link
        '''
        researchgate = Researchgate(profile, "site:researchgate.net")
        researchgate.search_author("researchgate.net/publication")
        researchgate.update_candidate(col, "researchgate_url")
        '''

        #Update Candidate scholar profile link
        scholargoogle = Scholar(profile, "site:scholar.google.com")
        scholargoogle.search_author("scholar.google.com/citations")
        scholargoogle.update_candidate(col, "googlescholar_url")

    else:
        print("The query didn't return any documents.")

    scholar_api=ScholarAPI(profile)
    scholar_api.check_papers()
    scholar_api.update_publication(col)
    scholar_api.update_researchgate_publication(col)
    # Update scholargoogle
    ####get the scholar url

    '''
    # Update researchgate
    researchgate = ResearchGateScraper(profile)
    researchgate.find_all_papers(researchgate.candinate['researchgate_url'], 1)
    researchgate.check_papers()
    researchgate.update_publication(col)
    researchgate.update_researchgate_publication(col)
    '''



