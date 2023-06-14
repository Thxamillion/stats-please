from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
import spacy
import os
import pickle
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')





# Load the English language model
nlp = spacy.load('en_core_web_lg')
querys = ["Lonnie walker stats with more than 20 minutes","anthony davis stats with less than 10 shots","austin reaves stats with more than 10 shots","how many threes did klay thompson make"]
def normalize_query(query):
    # Process the query with spaCy
    doc = nlp(query)

    # Find the PERSON entities (assumed to be player names)
    player_names = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
    print(player_names)

    # Lowercasing, lemmatization and punctuation removal
    normalized_query = []
    for token in doc:
        if not token.is_punct:
            # Convert to lowercase and use lemma for each token
            normalized_query.append(token.lemma_.lower())

    normalized_query = " ".join(normalized_query)

    # If there's only one player, rearrange the query to start with their name
    if len(player_names) == 1:
        # Remove the player's name from the query
        remaining_query = normalized_query.replace(player_names[0].lower(), '')
        return f"{player_names[0]} {remaining_query}"

    # If there are no players or more than two, return the normalized query
    return normalized_query


for query in querys:
    if query.lower() == "quit":
        break
    normalized_query = normalize_query(query)
    print(normalized_query)   # Get SQL query from OpenAI


