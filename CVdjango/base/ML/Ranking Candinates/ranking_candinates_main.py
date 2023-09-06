from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from CVdjango.base.scrapers.utils import *
from bson import ObjectId
from CVdjango.base.db.utils import *

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
    position=po
    try:
        # author have the stuff inside
        embeddings = []
        for pub in author["publication"]:
            # Loop through each source array and try to find a match
            for source_name in ['researchgate']:  # Add other sources as needed
                source_item = None
                source_item_index = None

                for index, item in enumerate(author.get(source_name, [])):
                    print(f"Checking item: {item}")
                    if item['url'] == pub.get(f"{source_name}_url"):
                        source_item = item
                        source_item_index = index
                        break

                if source_item:
                    if not source_item.get('embedding', []):
                        embedding = specter_embedding(pub['title'], '')
                        pub["embedding"] = embedding
                        print(embedding)
                        if source_item_index is not None:
                            print(embedding)
                            author[source_name][source_item_index]['embedding'] = embedding
    except Exception as error:
        print(error)
def normalization(value,min,max):
    return (value-min)/(max-min)

def mean_publications(authors):
    candidates_scores=[]
    for author in authors:
        author=publications_specter_embedding(author)
        sorted_data = sorted(author["publication"], key=lambda x: x['embedding'],reverse=True)
        # take the top N
        N = 1
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


def update_embedding(authors_or_author, db, col):
    # Check if the input is a list of dictionaries (for multiple authors)
    if isinstance(authors_or_author, list):
        for author in authors_or_author:
            try:
                updated_author = publications_specter_embedding(author)
                db.Candidate.update_one({"_id": updated_author['_id']}, {
                    "$set": {"publication": updated_author['publication'],
                             "researchgate": updated_author.get('researchgate', [])}})
            except Exception as e:
                print(f"An error occurred: {e}")

    # Check if the input is a single dictionary (for one author)
    elif isinstance(authors_or_author, dict):
        try:
            publications_specter_embedding(authors_or_author)
            print(authors_or_author.get('publication'))
            print(authors_or_author['publication'])
            # Update the document if the field has changed
            result = db.Candinates.update_one(
                {"_id": authors_or_author['_id']},
                {"$set": {
                    "publication": authors_or_author['publication'],
                    "researchgate": authors_or_author.get('researchgate', [])
                }}
            )
        except Exception as e:
            print(f"An error occurred: {e}")

    else:
        print(
            "Invalid input type. Expecting a dictionary (for a single author) or a list of dictionaries (for multiple authors).")


def rank_candidates(candidates_scores, threshold):
    print(candidates_scores)
    ranked_candidates = sorted(candidates_scores, key=lambda x: x["score"], reverse=True)
    return [c for c in ranked_candidates if c["score"] > threshold]



if __name__ == '__main__':
    mongo_handler = MongoDBHandler("localhost", 27017)
    client = mongo_handler.connect()
    # TODO SOS
    author = 'Elpiniki I Papageorgiou'

    if client:
        db, col = mongo_handler.get_database_and_collection('CVproject', 'Candinates')
        print(col)

        profile = mongo_handler.find_document_one(col, author)
        update_embedding(profile,db)
        #a=mean_publications(profile)
        #rank_candidates(a,0.6)