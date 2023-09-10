from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(embedding1, embedding2):
    return cosine_similarity(embedding1, embedding2)
def normalization(value,min,max):
    return (value-min)/(max-min)


def mean_publications(author,posittion_embedding):

    # take the top N
    N = 10
    if len(author["publication"])<N: N=len(author["publication"])
    estimation = 0
    sorted_data=[]
    for pub in author["publication"]:
        if pub['embedding']:
            print(compute_similarity( pub['embedding'],posittion_embedding )[0][0])
            sorted_data.append(compute_similarity( pub['embedding'],posittion_embedding )[0][0])

    top_N_values = sorted(sorted_data, reverse=True)[:N]
    # calculate the mean
    mean = sum(top_N_values)/N
    candidate_score={
        "id": author["_id"],
        "score":mean
    }
    return candidate_score


def rank_candidates(candidates_scores, threshold):
    print(candidates_scores)
    ranked_candidates = sorted(candidates_scores, key=lambda x: x["score"], reverse=True)
    return [c for c in ranked_candidates if c["score"] > threshold]