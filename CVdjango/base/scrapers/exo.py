from scholarly import scholarly

# search by unique author id
author_id = 'your_author_id_here'
author = scholarly.search_author_id(author_id)

# fill author including their publications
author_filled = scholarly.fill(author, sections=['indices', 'basics', 'publications'])

# print the filled author information
print(author_filled)

# get author's publications
for pub in author_filled['publications']:
    pub_filled = scholarly.fill(pub)
    try:
        print(f"Title: {pub_filled['bib']['title']}")
        print(f"Abstract: {pub_filled['abstract']}")
    except KeyError:
        print("Abstract not available.")
    print()