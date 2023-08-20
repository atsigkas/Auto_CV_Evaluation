from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from CVdjango.base.scrapers.utils import *

au={
    "publication":[{
        'title': 'Attention is all you need',
        'abstract': ' The dominant sequence transduction models are based on complex recurrent or convolutional neural networks',
        'year': 2018,
        'embedding': None
    },{
        'title': 'Attention was !!',
        'abstract': ' The dominant sequence transduction models are based on complex  network',
        'year': 2018,
        'embedding': None
    }]
}
po={
        'title': 'BERT',
        'abstract': 'We introduce a new language representation model called BERT'
}

def compute_similarity(embedding1, embedding2):
    return cosine_similarity(embedding1, embedding2)

def specter_embedding(title , abstract):
    tokenizer = AutoTokenizer.from_pretrained('allenai/specter')
    model = AutoModel.from_pretrained('allenai/specter')
    # concatenate title and abstract
    title_abs = title + tokenizer.sep_token + (abstract or '')
    # preprocess the input
    inputs = tokenizer(title_abs, padding=True, truncation=True, return_tensors="pt", max_length=512)
    result = model(**inputs)
    # take the first token in the batch as the embedding
    embeddings = result.last_hidden_state[:, 0, :]
    #print(embeddings)
    return embeddings.detach().numpy().tolist()


def publications_specter_embedding(author):
    author=au
    position=po
    try:
        # author have the stuff inside
        embeddings = []
        for pub in author["publication"]:
            if pub["embedding"] is None:
                pub["embedding"]=specter_embedding(pub['title'], pub['abstract'])
        # TODO update the author for a specific field
        return author
    except Exception as error:
        print("Error in the author_specter_embedding function.")
def normalization(value,min,max):
    return (value-min)/(max-min)

def mean_publications(authors):
    candidates_scores=[]
    for author in authors:
        author=publications_specter_embedding(author)
        sorted_data = sorted(author["publication"], key=lambda x: x['embedding'],reverse=True)
        # take the top N
        N = 10
        if len(author["publication"])<N: N=len(author["publication"])
        estimation = 0
        top = sorted_data[:N]
        for pub in sorted_data:
            print(compute_similarity(pub['embedding'],specter_embedding(po["title"],po["abstract"])), "BBBBBBBBBBBBBBB")
            estimation=estimation+ compute_similarity(pub['embedding'],specter_embedding(po["title"],po["abstract"]))[0][0] * 0.85 +0.15*normalization(pub["year"],1900,2023)
            print(estimation)
        # calculate the mean
        mean = estimation/N
        candidates_scores.append({
            "id":"4324",
            "score":mean
        })
    return candidates_scores
def rank_candidates(candidates_scores, threshold):
    print(candidates_scores)
    ranked_candidates = sorted(candidates_scores, key=lambda x: x["score"], reverse=True)
    return [c for c in ranked_candidates if c["score"] > threshold]

if __name__ == '__main__':
    a=mean_publications(au)
    rank_candidates(a,0.6)