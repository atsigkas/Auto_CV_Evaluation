from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(embedding1, embedding2):
    return cosine_similarity(embedding1, embedding2)
def normalization(value,min,max):
    return (value-min)/(max-min)

def mean_publications(author,posittion_embedding):

    sorted_data = sorted(author["publication"], key=lambda x: x['embedding'],reverse=True)
    # take the top N
    N = 2
    if len(author["publication"])<N: N=len(author["publication"])
    estimation = 0
    top = sorted_data[:N]
    for pub in top:
        print(compute_similarity(pub['embedding'],posittion_embedding))
        estimation = estimation + compute_similarity( pub['embedding'],posittion_embedding )
        print(estimation)
    # calculate the mean
    mean = estimation/N
    candidate_score={
        "id": author["_id"],
        "score":mean
    }
    return candidate_score
def rank_candidates(candidates_scores, threshold):
    print(candidates_scores)
    ranked_candidates = sorted(candidates_scores, key=lambda x: x["score"], reverse=True)
    return [c for c in ranked_candidates if c["score"] > threshold]