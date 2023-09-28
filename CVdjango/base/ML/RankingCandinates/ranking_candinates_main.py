from sklearn.metrics.pairwise import cosine_similarity

from ..Embedding.embedding import specter_embedding
from ...scrapers.SJR.SJR import search_type
from ...scrapers.CORE.CORE import check_csv_files

THRESHOLD=0
PUB_PERCENTAGE = 0.85
TYPE_PERCENTAGE = 0.15

def compute_similarity(embedding1, embedding2):
    return cosine_similarity(embedding1, embedding2)
def normalization(value,min,max):
    return (value-min)/(max-min)


def mean_publications(author,position_embedding,NotFoundPublications):


    length_of_publication = 0
    sorted_data = []
    rank = 0
    for notfoundpub in NotFoundPublications:
        for pub in author["publication"] :
            if notfoundpub['pub']['title'] == pub['title'] and author["_id"]==notfoundpub["id"]:
                pub['embedding'] = specter_embedding(pub['title'],'')
                print("TIME")

    for pub in author["publication"]:
        rank = 0
        if pub.get('embedding') and pub['embedding'] != '':
            text_similarity = compute_similarity(pub['embedding'], position_embedding)[0][0]
            length_of_publication += 1
            if pub.get('name_of_type') and pub["name_of_type"] != "Unknown":
                if pub["year"]:
                    rank = search_type(pub["name_of_type"], pub["year"])
                    if rank == 0:
                        rank = check_csv_files(pub["name_of_type"], pub["year"])
                        if rank == 0:
                            print("### NOT FOUND QUALITY METRIC")

            if rank > 0:
                text_similarity = text_similarity * PUB_PERCENTAGE
                rank_type = normalization(rank, 0, 100) * TYPE_PERCENTAGE
                sorted_data.append(text_similarity+rank_type)
            else:
                sorted_data.append(text_similarity)

    # calculate the mean
    print(f"Length :{length_of_publication}")
    mean = round(sum(sorted_data)/length_of_publication, 4)
    candidate_score = {
        "author": author["author"],
        "score": mean
    }
    return candidate_score


def rank_candidates(candidates_scores):
    print(candidates_scores)
    ranked_candidates = sorted(candidates_scores, key=lambda x: x["score"], reverse=True)
    return [c for c in ranked_candidates if c["score"] > THRESHOLD]