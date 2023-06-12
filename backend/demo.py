from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
import spacy
import os
import pickle
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')





# Load the English language model
nlp = spacy.load('en_core_web_lg')

def normalize_query(query):
    # Process the query with spaCy
    doc = nlp(query)
    print(doc)

    # Find the PERSON entities (assumed to be player names)
    player_names = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
    print(player_names)

    # If there are two players, assume it's a "vs" query

    # If there's only one player, rearrange the query to start with their name
    if len(player_names) == 1:
        # Remove the player's name from the query
        remaining_query = query.replace(player_names[0], '')
        return f"{player_names[0]} {remaining_query}"

    # If there are no players or more than two, return the original query
    return query


while True:
    query = input("Enter a query: ")
    if query.lower() == "quit":
        break
    normalized_query = normalize_query(query)
    print(normalized_query)   # Get SQL query from OpenAI

