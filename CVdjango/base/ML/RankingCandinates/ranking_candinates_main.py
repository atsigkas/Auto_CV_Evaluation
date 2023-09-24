from sklearn.metrics.pairwise import cosine_similarity
from ...scrapers.SJR.SJR import search_type

THRESHOLD=0
PUB_PERCENTAGE = 0.85
TYPE_PERCENTAGE = 0.15

def compute_similarity(embedding1, embedding2):
    return cosine_similarity(embedding1, embedding2)
def normalization(value,min,max):
    return (value-min)/(max-min)


def mean_publications(author,position_embedding):


    length_of_publication = 0
    sorted_data = []
    rank = 0

    for pub in author["publication"]:
        rank = 0
        if pub['embedding']:
            text_similarity = compute_similarity(pub['embedding'], position_embedding)[0][0]

            if pub["name_of_type"] != "Unknown":
                if pub["year"]:
                    rank=search_type(pub["name_of_type"], pub["year"])
            if rank > 0:
                text_similarity = text_similarity * PUB_PERCENTAGE
                rank_type = normalization(rank, 0, 100) * TYPE_PERCENTAGE
                sorted_data.append(text_similarity+rank_type)
            else:
                sorted_data.append(text_similarity)

    # calculate the mean
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