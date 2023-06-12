import os
import openai
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Cache
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')
POSTGRE_URL = os.getenv('POSTGRE_URL')

engine = create_engine(POSTGRE_URL)




# Set the OpenAI API key
openai.api_key = OPENAI_KEY



def get_sql_query(query):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Check if the query is already cached
        cache = session.query(Cache).filter(Cache.user_query == query).one_or_none()

        if cache is not None:
            print('Fetching from cache')
            # Query is in cache, so return the cached result
            return cache.sql_response
        else:
            print('Fetching from API')
            # Query is not in cache, so fetch it from the API
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt="###postgres SQL tables, with their properties:\n\n game(id, date, day)\n#\officials(id, game_id, official_id, first_name, last_name, jersey_num, name)\n#\player_stats(id, game_id, team_id, team_abbreviation, team_city, player_id, player_name, nickname, start_position, comment, minutes, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct, ftm, fta, ft_pct, oreb, dreb, reb, ast, stl, blk, to, pf, pts, plus_minus)\n#\team_stats(id, game_id, team_id, team_name, team_abbreviation, team_city, status, minutes, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct, ftm, fta, ft_pct, oreb, dreb, reb, ast, stl, blk, to, pf, pts, plus_minus)\n#\n##\n\nexample query = Austin reaves stats with 10 or more shots \n\nSELECT pts,fg_pct, ast, reb, stl,blk, plus_minus\nFROM player_stats\nWHERE player_name = 'Austin Reaves'\nAND fga > 10;\n\nexample query = Show me anthony davis vs Nikola jokic stats\n\nSELECT \n    player_stats.player_name, \n    player_stats.pts, \n    player_stats.fg_pct, \n    player_stats.ast, \n    player_stats.reb, \n    player_stats.stl,\n    player_stats.blk, \n\tplayer_stats.minutes, \n    player_stats.plus_minus\n\t\nSELECT \n    ps1.player_name, \n    ps1.pts, \n    ps1.fg_pct, \n    ps1.ast, \n    ps1.reb, \n    ps1.stl,\n    ps1.blk, \n    ps1.plus_minus\nFROM \n    player_stats AS ps1\nJOIN \n    player_stats AS ps2 ON ps1.game_id = ps2.game_id\nWHERE \n    (ps1.player_name = 'Anthony Davis' AND ps2.player_name = 'Nikola Jokic')\nOR\n    (ps1.player_name = 'Nikola Jokic' AND ps2.player_name = 'Anthony Davis');\n\n" + query,
                temperature=0.2,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            result = response.choices[0].text.strip()

            # Save the result to the cache
            cache = Cache(user_query=query, sql_response=result)
            session.add(cache)
            session.commit()
            print("Added to cache")
            return result
    except:
        session.rollback()
        raise
    finally:
        session.close()
            
    





   
    
## commented out for server
# while True:
#     query = input("Enter a query: ")
#     if query.lower() == "quit":
#         break
#     for i in range(2):
#         start_time = time.time()
#         sql_query = get_sql_query(query)   # Get SQL query from OpenAI
#         print("Time consuming: {:.2f}s".format(time.time() - start_time))
        
#         print(f"Generated SQL Query: {sql_query}")
   