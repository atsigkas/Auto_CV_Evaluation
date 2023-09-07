from CVdjango.base.ML.Embedding.embedding import *
from CVdjango.base.db.utils import *
from CVdjango.base.scrapers.ResearchGate.researchgate import *
from CVdjango.base.scrapers.ResearchGate.researchgate_scraper import *
from CVdjango.base.scrapers.Scholar.scholar import *
from CVdjango.base.scrapers.Scholar.scholar_api import *
from CVdjango.base.scrapers.candidate import *
from CVdjango.base.scrapers.Position import *
from CVdjango.base.ML.RankingCandinates.ranking_candinates_main import *



RESEARCHGATE=True
GOOGLE=False

mongo_handler = MongoDBHandler("localhost", 27017)
client = mongo_handler.connect()

#title="SVM-based fuzzy decision trees for classification of high spatial resolution remote sensing images"
#title2="Right Ventricular Volume Prediction by Feature Tokenizer Transformer-Based Regression of 2D Echocardiography Small-Scale Tabular Data"
title='Uncovering the Black Box of Coronary Artery Disease Diagnosis: The Significance of Explainability in Predictive Models'
title2='Classification models for assessing coronary artery disease instances using clinical and biometric data: an explainable man-in-the-loop approach'
candidate = {
                "author": "Elpiniki I Papageorgiou",
                "email": "a@a.gr",
                "phone": "53453",
                "researchgate_url": '',
                "googlescholar_url": '',
                "sematic_url": '',
                "publication": [
                    {
                        "title": title,
                        "abstract":'',
                        "researchgate_url": '',
                        "googlescholar_url": '',
                        "sematic_url": '',
                    },
                    {
                        "title": title2,
                        "abstract":'',
                        "researchgate_url": '',
                        "googlescholar_url": '',
                        "sematic_url": '',
                        "embedding" : ''
                    }
                ]
            }

candidates_score=[]
if client:
    db, col = mongo_handler.get_database_and_collection('CVproject', 'Candinates')
    profile = mongo_handler.find_document_one(col, candidate["author"])

    if profile:
        print(f"The query  some Documents for the Candidate '{profile['author']}'.")
        can = Candidate(profile)

        # Convert arrays to sets of serialized objects
        old_set = set(obj["title"] for obj in can.candidate["publication"])
        new_set = set(obj["title"] for obj in candidate["publication"])

        # Find objects that are in old array but not in new array
        removed_publications = old_set - new_set

        # Find objects that are in new array but not in old array
        added_publications = new_set - old_set

        print(f"Number of Publication from old Resume : "+str(len(removed_publications)))
        print(f"Number of Publication from New Resume which wasn't in the Array : "+str(len(added_publications)))

        #Remove the old Publications
        filtered_old_array = [obj for obj in can.candidate["publication"] if obj["title"] not in removed_publications]
        can.candidate["publication"]= filtered_old_array

        # Convert the new ones
        added_objects_array = [{
            "title": obj,
            "abstract":'',
            "researchgate_url": '',
            "googlescholar_url": '',
            "sematic_url": ''
        } for obj in added_publications]

        # New Publications
        for new in added_objects_array:
            print(f"Checking item: {new}")
            for source_name in ['researchgate',"googlescholar"]:
                for index, item in enumerate(can.candidate.get(source_name, [])):
                    if item['title'] == new["title"]:
                        source_item = item
                        source_item_index = index
                        break

                if source_item and source_item_index is not None:
                    new[source_name+"_url"]=source_item["url"]
                    new["abstract"] = source_item["abstract"]
                    if not source_item.get('embedding', []):
                        embedding = specter_embedding(new['title'], new['abstract'])
                        new["embedding"] = embedding
                        print(embedding)
                        if source_item_index is not None:
                            print(embedding)
                            can.candidate[source_name][source_item_index]['embedding'] = embedding
                    else:
                        new["embedding"] = source_item["embedding"]

            can.candidate["publication"].append(new)

        if len(removed_publications)>0 or len(added_publications)>0:
            can.update_candidate(col)

        po = {
            'title': 'BERT',
            'abstract': 'We introduce a new language representation model called BERT'
        }
        position = Position('BERT', 'We introduce a new language representation model called BERT')
        posittion_embedding = specter_embedding(position.title, position.abstract)
        print(mean_publications(can.candidate, posittion_embedding))

    else:
        print("Insert the author")
        can=Candidate()
        if RESEARCHGATE:
            researchgate = Researchgate(candidate, "site:researchgate.net")
            researchgate.search_author("researchgate.net/publication")

            researchgate = ResearchGateScraper(researchgate.candidate)
            url="https://www.researchgate.net/"+researchgate.candidate['researchgate_url']
            researchgate.find_all_papers(url, 1)
            researchgate.check_papers()

            can.override_data(researchgate.candidate)

        if GOOGLE:
            scholargoogle = Scholar(candidate, "site:scholar.google.com")
            scholargoogle.search_author("scholar.google.com/citations")

            scholar_api=ScholarAPI(candidate)
            scholar_api.check_papers()

            can.override_data(scholar_api.candidate)

        can.insert_candidate(col)

        publications_specter_embedding(can.candidate)
        update_embedding(can.candidate, col)


