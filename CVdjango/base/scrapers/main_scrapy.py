from .CORE.CORE import core_crawling
from ..db.utils import *
from .utils import json_serial
from .ResearchGate.researchgate import *
from .ResearchGate.researchgate_scraper import *
from .Scholar.scholar import *
from .Scholar.scholar_api import *
from .Candidate import *
from .Position import *
from ..ML.RankingCandinates.ranking_candinates_main import *
import threading
import time
import json
from bson import ObjectId



RESEARCHGATE = True
GOOGLE = False
THREADING = False


def process_candidate(candidate,mongo_handler,client):
    print(f"The Author : '{candidate['name']}'.")
    if client:
        found = False
        db, col = mongo_handler.get_database_and_collection('CVproject', 'Candinates')
        profiles = mongo_handler.find_document(col,candidate)
        finding_results = []
        for i in profiles:
            finding_results.append(i)
        if finding_results:
            for profile in finding_results:
                if found:
                    break
                if (profile['email'] == candidate["email"] and candidate["email"] != "Unknown") or (profile['phone'] == candidate["phone"] and candidate["phone"] != "Unknown"):
                    found = True
                    break
                for pub in candidate["publications"]:
                    if found:  # Check the flag at the start of the outer loop
                        break
                    for pub_in_database in profile["researchgate"]:
                        if pub['title'] == pub_in_database['title'] and profile["name"] == candidate["name"]:
                            found = True
                            break

            if found:
                print(f"The query  some Documents for the Candidate '{profile['name']}'.")
                can = Candidate(profile)

                old_set = set(obj["title"] for obj in can.candidate["publications"])
                new_set = set(obj["title"] for obj in candidate["publications"])

                removed_publications = old_set - new_set

                added_publications = new_set - old_set

                print(f"Number of Publications from Old Resume which weren't in the new one : "+str(len(removed_publications)))
                print(f"Number of Publications from New Resume which weren't in the old one : "+str(len(added_publications)))

                #Remove the old Publications
                filtered_old_array = [obj for obj in can.candidate["publications"] if obj["title"] not in removed_publications]
                can.candidate["publications"]= filtered_old_array

                # Convert the new ones
                added_objects_array = [{
                    "title": obj,
                    "abstract":'',
                    "researchgate_url": '',
                    "googlescholar_url": '',
                    "sematic_url": ''
                } for obj in added_publications]

                # New Publication
                source_item = None
                source_item_index = None
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

                    can.candidate["publications"].append(new)

                if len(removed_publications)>0 or len(added_publications)>0:
                    can.update_candidate(col)
            else:
                print(f"The Author wasn't found : '{candidate['name']}'.")

        else:
            if candidate['name'] is not None:
                if len(candidate["publications"])>0:
                    print("Insert the author")
                    can = Candidate()
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
                else:
                    can = Candidate(candidate)
                    can.insert_candidate(col)


def find_candidate(candidates):
    start_time = time.time()
    core_crawling()

    # DB connection
    mongo_handler = MongoDBHandler("localhost", 27017)
    client = mongo_handler.connect()

    if THREADING:
        threads = []
        for candidate in candidates:
            t = threading.Thread(target=process_candidate, args=(candidate, mongo_handler, client))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
    else:
        for candidate in candidates:
            process_candidate(candidate,mongo_handler,client)



    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time} seconds")

    return transform_data_for_frontend(candidates,mongo_handler,client)


def transform_data_for_frontend(candidates,mongo_handler,client):
    updated_candidates=[]
    for candidate in candidates:
        print(f"The Author : '{candidate['name']}'.")
        if client:
            found = False
            db, col = mongo_handler.get_database_and_collection('CVproject', 'Candinates')
            profiles = mongo_handler.find_document_after_pdfs(col, candidate)
            finding_results = []
            for i in profiles:
                finding_results.append(i)
            if finding_results:
                for profile in finding_results:
                    if found:
                        break
                    if (profile['email'] == candidate["email"] and candidate["email"] != "Unknown") or (
                            profile['phone'] == candidate["phone"] and candidate["phone"] != "Unknown"):
                        found = True
                        break
                    for pub in candidate["publications"]:
                        if found:  # Check the flag at the start of the outer loop
                            break
                        for pub_in_database in profile["researchgate"]:
                            if pub['title'] == pub_in_database['title'] and profile["name"] == candidate["name"]:
                                found = True
                                break
                if found:
                    print(f"The query  some Documents for the Candidate '{profile['name']}'.")
                    totalarticles = 0
                    totalconference = 0
                    for pub in profile["publications"]:
                        if "type" in pub:
                            type_pub = pub['type'].lower()
                            if type_pub == "article" or type_pub == "journal" :
                                totalarticles += 1

                            if type_pub == "conference paper" or type_pub == "conference":
                                totalconference += 1
                    can={
                        "candidate":Candidate(profile).to_dict()["candidate"],
                        "totalArticles" : totalarticles,
                        "totalConference": totalconference
                    }

                    updated_candidates.append(json.loads(json.dumps(can, default=json_serial, indent= None)))
    return updated_candidates


def update_candidate_profile(_id, url_updated):
    mongo_handler = MongoDBHandler("localhost", 27017)
    client = mongo_handler.connect()
    if client:
        db, col = mongo_handler.get_database_and_collection('CVproject', 'Candinates')
        profile = mongo_handler.find_document_one(col, "_id", ObjectId(_id))
        if profile:
            print("Update the author")
            can = Candidate(profile)
            if "researchgate.net" in url_updated:
                profile["researchgate_url"] = url_updated
                researchgate = Researchgate(profile, "site:researchgate.net")
                researchgate = ResearchGateScraper(researchgate.candidate)
                researchgate.find_all_papers(researchgate.candidate['researchgate_url'], 1)
                researchgate.check_papers()

                can.override_data(researchgate.candidate)

            if "scholar.google.com" in url_updated:
                profile["googlescholar_url"] = url_updated
                scholar_api = ScholarAPI(profile)
                scholar_api.check_papers()

                can.override_data(scholar_api.candidate)

            publications_specter_embedding(can.candidate)
            can.update_candidate_after_url(col)

            totalarticles = 0
            totalconference = 0
            for pub in profile["publications"]:
                if "type" in pub:
                    type_pub = pub['type'].lower()
                    if type_pub == "article" or type_pub == "journal":
                        totalarticles += 1

                    if type_pub == "conference paper" or type_pub == "conference":
                        totalconference += 1
            candinate = {
                "candidate": can.to_dict()["candidate"],
                "totalArticles": totalarticles,
                "totalConference": totalconference
            }

            return(json.loads(json.dumps(candinate, default=json_serial, indent=None)))
