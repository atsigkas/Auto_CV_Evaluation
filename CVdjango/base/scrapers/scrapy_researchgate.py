from CVdjango.base.ML.Embedding.embedding import publications_specter_embedding
from CVdjango.base.ML.Embedding.embedding import update_embedding
from CVdjango.base.db.utils import *
from CVdjango.base.scrapers.ResearchGate.researchgate import *
from CVdjango.base.scrapers.ResearchGate.researchgate_scraper import *
from CVdjango.base.scrapers.Scholar.scholar import *
from CVdjango.base.scrapers.Scholar.scholar_api import *
from CVdjango.base.scrapers.candidate import *



GATE=True
GOOGLE=True

mongo_handler = MongoDBHandler("localhost", 27017)
client = mongo_handler.connect()
# TODO SOS

title="SVM-based fuzzy decision trees for classification of high spatial resolution remote sensing images"
title2="Right Ventricular Volume Prediction by Feature Tokenizer Transformer-Based Regression of 2D Echocardiography Small-Scale Tabular Data"
candidate = {
                "author": "Serafeim Moustakidis",
                "email": "a@a.gr",
                "phone": "53453",
                "researchgate_url": '',
                "googlescholar_url": '',
                "sematic_url": '',
                "publication": [
                    {
                        "title": title,
                        "researchgate_url": '',
                        "googlescholar_url": '',
                        "sematic_url": '',
                    },
                    {
                        "title": title2,
                        "researchgate_url": '',
                        "googlescholar_url": '',
                        "sematic_url": '',
                        "embedding" : ''
                    }
                ]
            }

if client:
    db, col = mongo_handler.get_database_and_collection('CVproject', 'Candinates')
    # TODO Find
    # check which url is empty
    # if it is empty then we have to run it
    # TODO Insert after the PDF

    # ok = mongo_handler.insert_one_document(col)
    profile = mongo_handler.find_document_one(col, candidate["author"])

    if profile:
        print(f"The query  some Documents for the Candidate '{profile['author']}'.")
        can = Candidate(profile)

        # Convert arrays to sets of serialized objects
        old_set = set(obj["title"] for obj in can.candidate["publication"])
        new_set = set(obj["title"] for obj in candidate["publication"])

        print(old_set)
        print(new_set)
        # Find objects that are in old array but not in new array
        removed_objects = old_set - new_set
        # Convert back to list of objects]

        # Find objects that are in new array but not in old array
        added_objects = new_set - old_set
        # Convert back to list of objects

        print(len(removed_objects))
        print(len(added_objects))

        filtered_old_array = [obj for obj in can.candidate["publication"] if obj["title"] not in removed_objects]


        #publications_specter_embedding(can.candidate)
        #update_embedding(can.candidate, col)

    else:
        print("Insert the author")
        can=Candidate()
        if GATE:
            researchgate = Researchgate(candidate, "site:researchgate.net")
            researchgate.search_author("researchgate.net/publication")
            #researchgate.update_candidate(col, "researchgate_url")
            print(researchgate.candidate['researchgate_url'])

            researchgate = ResearchGateScraper(researchgate.candidate)
            url="https://www.researchgate.net/"+researchgate.candidate['researchgate_url']
            researchgate.find_all_papers(url, 1)
            researchgate.check_papers()

            #researchgate.update_publication(col)
            #researchgate.update_researchgate_publication(col)
            #researchgate.insert_researchgate_candidate(col)
            can.override_data(researchgate.candidate)


        if GOOGLE:
            scholargoogle = Scholar(candidate, "site:scholar.google.com")
            scholargoogle.search_author("scholar.google.com/citations")
            #scholargoogle.update_candidate(col, "googlescholar_url")

            scholar_api=ScholarAPI(candidate)
            scholar_api.check_papers()
            #scholar_api.update_publication(col)
            #scholar_api.update_googlescholar_publication(col)
            #scholar_api.insert_researchgate_candidate(col)
            can.override_data(scholar_api.candidate)

        can.insert_candidate(col)

        publications_specter_embedding(can.candidate)
        update_embedding(can.candidate, col)


