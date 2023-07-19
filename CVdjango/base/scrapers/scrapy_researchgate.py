from CVdjango.base.db.utils import *
from CVdjango.base.scrapers.extract_info_publication_researchgate import *
from CVdjango.base.scrapers.search_author_researchgate import *
from CVdjango.base.scrapers.researchgate import *
from CVdjango.base.scrapers.scholar import *


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

    # ok = mongo_handler.insert_one_document(col)
    profile = mongo_handler.find_document_one(col, author)
    if profile:
        print("The query returned some documents.")
        #update ResearchGate
        researchgate = Researchgate(profile, "site:researchgate.net")
        researchgate.search_author("researchgate.net/publication")
        researchgate.update_candidate(col, "researchgate_url")
        #update Scholar
        researchgate = Scholar(profile, "site:scholar.google.com")
        researchgate.search_author("scholar.google.com/citations")
        researchgate.update_candidate(col, "researchgate_url")
    else:
        print("The query didn't return any documents.")
    '''
    profile = mongo_handler.find_document_one(col,author)
    researchgate = ResearchGateScraper(profile)
    researchgate.find_all_papers(researchgate.candinate['researchgate_url'], 1)
    researchgate.check_papers()

    print(researchgate.candinate)
    researchgate.update_publication(col)
    researchgate.update_researchgate_publication(col)
    '''