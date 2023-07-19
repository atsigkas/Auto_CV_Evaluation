from CVdjango.base.db.utils import *
from CVdjango.base.scrapers.regate import *
from CVdjango.base.scrapers.runspiders import *



mongo_handler = MongoDBHandler("localhost", 27017)
client = mongo_handler.connect()
# TODO SOS
author = 'Athanasios Anagnostis'



if client:
    db, col = mongo_handler.get_database_and_collection('CVproject', 'Candinates')
    #TODO Find if exist then insert
    #TODO Insert after the PDF

    #ok = mongo_handler.insert_one_document(col)
    profile = mongo_handler.find_document_one(col, author)

    candinate = search_author(profile['author'],
                              profile['publication'][0]['title'],
                              'site:researchgate.net')
    update_candinate(col,candinate,profile['_id'])

    profile = mongo_handler.find_document_one(col,author)
    researchgate = ResearchGateScraper(profile)
    researchgate.find_all_papers(researchgate.candinate['researchgate_url'], 1)
    researchgate.check_papers()

    print(researchgate.candinate)
    researchgate.update_publication(col)
    researchgate.update_researchgate_publication(col)
