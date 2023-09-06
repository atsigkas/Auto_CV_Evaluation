from transformers import AutoTokenizer, AutoModel

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

def update_embedding(authors_or_author, col):
    # Check if the input is a list of dictionaries (for multiple authors)
    if isinstance(authors_or_author, list):
        for author in authors_or_author:
            try:
                #updated_author = publications_specter_embedding(author)
                col.update_one({"_id": authors_or_author['_id']}, {
                    "$set": {"publication": authors_or_author['publication'],
                             "researchgate": authors_or_author.get('researchgate', [])}})
            except Exception as e:
                print(f"An error occurred: {e}")

    # Check if the input is a single dictionary (for one author)
    elif isinstance(authors_or_author, dict):
        try:
            print(authors_or_author.get('publication'))
            print(authors_or_author['publication'])
            # Update the document if the field has changed
            result = col.update_one(
                {"_id": authors_or_author['_id']},
                {"$set": {
                    "publication": authors_or_author['publication'],
                    "researchgate": authors_or_author.get('researchgate', [])
                }}
            )
        except Exception as e:
            print(f" update_embedding - An error occurred: {e}")

    else:
        print(
            "Invalid input type. Expecting a dictionary (for a single author) or a list of dictionaries (for multiple authors).")