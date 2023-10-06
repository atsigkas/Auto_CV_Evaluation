from .ML.Embedding.embedding import specter_embedding
from .ML.RankingCandinates.ranking_candinates_main import rank_candidates, mean_publications
from .ResumeParser.ExtractInfo_part1_python.pdf_extractor import process_pdfs
from .Scrapers import main_scrapy
from .Scrapers.Candidate import Candidate
from .Scrapers.Position import Position
import json


def find_candidate():
    directory = r"C:\Users\stav_\Desktop\projects\Auto_CV_Evaluation\CVdjango\uploads"
    # Process PDFs in the directory

    all_data = process_pdfs(directory)

    # Print all the extracted information for each PDF
    for data in all_data:
        print("##### EXTRACTION PHASE: ##### ")
        print("____________")
        if data['name']:
            print("____________")
            print(f"Name: {data['name']}")
            print(f"Email: {data['email']}")
            print(f"Phone : {data['phone']}")
            print("Publications extracted using regex:")
            if data["publications"] is not None:
                for pub in data["publications"]:
                    print(json.dumps(pub['title'], indent=4))
        else:
            print('No Name was found')
        print("____________")
    return main_scrapy.find_candidate(all_data)


def ranking(NotFoundPublications,candidates,positionTitle,positionDescription):
    candidates_scores = []
    position = Position(positionTitle, positionDescription)
    position_embedding = specter_embedding(position.title, position.abstract)
    for profile in candidates:
        print(f"The candidate is the {profile['candidate']['name']}")
        can = Candidate(profile["candidate"])
        candidates_scores.append(mean_publications(can.candidate, position_embedding,NotFoundPublications))
    return rank_candidates(candidates_scores)

