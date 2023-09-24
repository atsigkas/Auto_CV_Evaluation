from ..db.utils import *
from .ResearchGate.researchgate import *
from .ResearchGate.researchgate_scraper import *
from .Scholar.scholar import *
from .Scholar.scholar_api import *
from .candidate import *
from .Position import *
from ..ML.RankingCandinates.ranking_candinates_main import *
import threading
import time
import printjson

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

RESEARCHGATE = True
GOOGLE = False
THREADING = False

def process_candidate(candidate,mongo_handler,client,position,candidates_scores):
    print(f"The Author : '{candidate['author']}'.")
    if client:
        found = False
        db, col = mongo_handler.get_database_and_collection('CVproject', 'Candinates')
        profiles = mongo_handler.find_document(col,candidate)
        finding_results = []
        for i in profiles:
            finding_results.append(i)
        if finding_results:
            for profile in finding_results:
                print(profile['email'] )
                print(candidate["email"])
                if found:
                    break
                if profile['email'] == candidate["email"] or profile['phone'] == candidate["phone"]:
                    found = True
                    break
                for pub in candidate["publication"]:
                    if found:  # Check the flag at the start of the outer loop
                        break
                    for pub_in_database in profile["researchgate"]:
                        if pub['title'] == pub_in_database['title']:
                            found = True
                            break

            if found:
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
                                if source_item_index is not None:
                                    #print(embedding)
                                    can.candidate[source_name][source_item_index]['embedding'] = embedding
                            else:
                                new["embedding"] = source_item["embedding"]

                    can.candidate["publication"].append(new)

                if len(removed_publications)>0 or len(added_publications)>0:
                    can.update_candidate(col)

                position_embedding = specter_embedding(position.title, position.abstract)
                candidates_scores.append(mean_publications(can.candidate,position_embedding))
            else:
                print(f"The Author wasn't found : '{candidate['author']}'.")

        else:
            if candidate['author'] is not None:
                print("Insert the author")
                can=Candidate()
                if RESEARCHGATE:
                    researchgate = Researchgate(candidate, "site:researchgate.net")
                    researchgate.search_author("researchgate.net/publication")

                    researchgate = ResearchGateScraper(researchgate.candidate)
                    # TODO an den exei bre8ei researchgate.candidate['researchgate_url'
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
                position_embedding = specter_embedding(position.title, position.abstract)
                candidates_scores.append(mean_publications(can.candidate, position_embedding))


def find_ranking(position_title,position_description,candidates):
    start_time = time.time()
    mongo_handler = MongoDBHandler("localhost", 27017)
    client = mongo_handler.connect()
    candidates_scores = []
    position = Position(position_title, position_description)

    if THREADING:
        # List to hold all threads
        threads = []
        for candidate in candidates:
            t = threading.Thread(target=process_candidate, args=(candidate, mongo_handler,client,position,candidates_scores))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
    else:
        for candidate in candidates:
            process_candidate(candidate,mongo_handler,client,position,candidates_scores)

    ranked = rank_candidates(candidates_scores)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time} seconds")
    return ranked

