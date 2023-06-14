import os
import openai
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from db.models import Cache
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')
POSTGRE_URL = os.getenv('POSTGRE_URL')

engine = create_engine(POSTGRE_URL)




# Set the OpenAI API key
openai.api_key = OPENAI_KEY



def execute_sql_query(query):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Execute the query and fetch all results
        t = text(query)
        result_proxy = session.execute(t)
        session.commit()

        # Convert RowProxy objects to dictionaries
        result = [{column: value for column, value in zip(result_proxy.keys(), rowproxy)} for rowproxy in result_proxy]

    except:
        session.rollback()
        raise
    finally:
        session.close()

    return result


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
            prompt="\"Nba database schemas are below. Convert English queries to SQL queries:\n\n games(id, date, day)\n#\n#\n officials(id, game_id, official_id, first_name, last_name, jersey_num, name)\n#\n player_stats(id, game_id, team_id, team_abbreviation, team_city, player_id, player_name, nickname, start_position, comment, minutes, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct, ftm, fta, ft_pct, oreb, dreb, reb, ast, stl, blk, to, pf, pts, plus_minus)\n#\n team_stats(id, game_id, team_id, team_name, team_abbreviation, team_city, status, minutes, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct, ftm, fta, ft_pct, oreb, dreb, reb, ast, stl, blk, to, pf, pts, plus_minus)\n#\n##\"\n\n" + query + "\n\nexample: Austin reaves stats with 10 or more shots\noutput:SELECT pts,fg_pct, ast, reb, stl,blk, plus_minus FROM player_stats WHERE player_name = 'Austin Reaves' AND fga > 10;\n\nexample: Show me anthony davis vs Nikola jokic stats\noutput: SELECT player_stats.player_name, player_stats.pts,  player_stats.fg_pct,  player_stats.ast, player_stats.reb,  player_stats.stl,  player_stats.blk, player_stats.minutes,  player_stats.plus_minus\nSELECT ps1.player_name,  ps1.pts,  ps1.fg_pct,  ps1.ast,  ps1.reb,  ps1.stl, ps1.blk,  ps1.plus_minus\nFROM  player_stats AS ps1 JOIN  player_stats AS ps2 ON ps1.game_id = ps2.game_id WHERE \n    (ps1.player_name = 'Anthony Davis' AND ps2.player_name = 'Nikola Jokic') OR\n    (ps1.player_name = 'Nikola Jokic' AND ps2.player_name = 'Anthony Davis');\n\nexample: give me celtics record when scott foster is a ref\noutput: SELECT  games.date,  team_stats.team_name,  team_stats.team_abbreviation, team_stats.team_city,  team_stats.status,  team_stats.pts,  team_stats.plus_minus FROM  games JOIN \n  team_stats ON games.id = team_stats.game_id JOIN officials ON games.id = officials.game_id WHERE officials.first_name = 'Scott' AND  officials.last_name = 'Foster' AND  team_stats.team_abbreviation = 'BOS'; SELECT \n\n\n" + query,
            temperature=0,
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
            print(result)
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
   