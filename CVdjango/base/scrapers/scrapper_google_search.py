from CVdjango.base.db.utils import *
from CVdjango.base.scrapers.extract_info_publication_researchgate import *
from CVdjango.base.scrapers.search_author_researchgate import *



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
        candidate = search_author(profile, 'site:scholar.google.com')
        update_candidate(col, candidate)
    else:
        print("The query didn't return any documents.")