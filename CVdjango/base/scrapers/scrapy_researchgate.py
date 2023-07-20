from CVdjango.base.db.utils import *
from CVdjango.base.scrapers.researchgate_scraper import *
from CVdjango.base.scrapers.google_search import *
from CVdjango.base.scrapers.researchgate import *
from CVdjango.base.scrapers.scholar import *
from CVdjango.base.scrapers.scholar_api import *


mongo_handler = MongoDBHandler("localhost", 27017)
client = mongo_handler.connect()
# TODO SOS
author = 'Athanasios Anagnostis'

if client:
    db, col = mongo_handler.get_database_and_collection('CVproject', 'Candinates')
    # TODO Find
    # check which url is empty
    # if it is empty then we have to run it
    # TODO Insert after the PDF
    '''
    # ok = mongo_handler.insert_one_document(col)
    profile = mongo_handler.find_document_one(col, author)
    if profile:
        print("The query returned some Documents.")
        #update ResearchGate

        researchgate = Researchgate(profile, "site:researchgate.net")
        researchgate.search_author("researchgate.net/publication")
        researchgate.update_candidate(col, "researchgate_url")

        #update ScholarGoogle
        researchgate = Scholar(profile, "site:scholar.google.com")
        researchgate.search_author("scholar.google.com/citations")
        researchgate.update_candidate(col, "googlescholar_url")
    else:
        print("The query didn't return any documents.")
    '''
    profile = mongo_handler.find_document_one(col, author)
    a=ResearchGateScraper(profile)
    a.check_papers()
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


