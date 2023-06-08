from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Game, Official, PlayerStats, TeamStats
import json
import datetime
import os

engine = create_engine('postgresql:')

def log_message(message):
    with open('process.log', 'a') as log_file:
        log_file.write(f'{message}\n')

def log_error(error_message):
    with open('error.log', 'a') as error_file:
        error_file.write(f'{error_message}\n')


Base.metadata.create_all(engine)

# Create a Session object to interact with the database.
Session = sessionmaker(bind=engine)
session = Session()

# Load data from a JSON file

for last_four in range(3, 1231):  
    last_four_str = str(last_four).zfill(4)  # Fill with leading zeros to get 4 digits.
    game_id_str = f'002220{last_four_str}'  # Concatenate to get complete game_id.
    file_name = f'../api/game_{game_id_str}.json'


    
    if not os.path.exists(file_name):
        log_error(f'File {file_name} does not exist')
        continue

    try:
        log_message(f"Processing file: {file_name}")
        with open(file_name) as f:
            game_data = json.load(f)

        log_message(f"Opened file: {file_name}")
        game_id = game_data["PlayerStats"][0]["GAME_ID"]
        date_string = game_data['GAME_DATE']

        game_date = datetime.datetime.strptime(date_string, '%A, %B %d, %Y')
        day = game_date.strftime('%A')
        formatted_date = game_date.strftime('%m/%d/%Y')

        game = Game(id=game_id, date=formatted_date, day=day)
        session.add(game)
        log_message(f"Added game: {game_id}")

        for official in game_data['OFFICIALS']:
            session.add(Official(game_id=game_id, 
                official_id=official['OFFICIAL_ID'],
                first_name=official['FIRST_NAME'],
                last_name=official['LAST_NAME'],
                jersey_num=official['JERSEY_NUM']
            ))

        for player_stat in game_data['PlayerStats']:
            session.add(PlayerStats(
                game_id=game_id,
                team_id=player_stat['TEAM_ID'],
                team_abbreviation=player_stat['TEAM_ABBREVIATION'],
                team_city=player_stat['TEAM_CITY'],
                player_id=player_stat['PLAYER_ID'],
                player_name=player_stat['PLAYER_NAME'],
                nickname=player_stat['NICKNAME'],
                start_position=player_stat['START_POSITION'],
                comment=player_stat['COMMENT'],
                minutes=player_stat['MIN'],
                fgm=player_stat['FGM'],
                fga=player_stat['FGA'],
                fg_pct=player_stat['FG_PCT'],
                fg3m=player_stat['FG3M'],
                fg3a=player_stat['FG3A'],
                fg3_pct=player_stat['FG3_PCT'],
                ftm=player_stat['FTM'],
                fta=player_stat['FTA'],
                ft_pct=player_stat['FT_PCT'],
                oreb=player_stat['OREB'],
                dreb=player_stat['DREB'],
                reb=player_stat['REB'],
                ast=player_stat['AST'],
                stl=player_stat['STL'],
                blk=player_stat['BLK'],
                to=player_stat['TO'],
                pf=player_stat['PF'],
                pts=player_stat['PTS'],
                plus_minus=player_stat['PLUS_MINUS']
            ))

        for team_stat in game_data['TeamStats']:
            plus_minus = team_stat['PLUS_MINUS']
            if plus_minus < 0:
                status = 'Loss'
            elif plus_minus > 0:
                status = 'Win'

            session.add(TeamStats(
                game_id=game_id,
                team_id=team_stat['TEAM_ID'],
                team_name=team_stat['TEAM_NAME'],
                team_abbreviation=team_stat['TEAM_ABBREVIATION'],
                team_city=team_stat['TEAM_CITY'],
                minutes=team_stat['MIN'],
                fgm=team_stat['FGM'],
                fga=team_stat['FGA'],
                fg_pct=team_stat['FG_PCT'],
                fg3m=team_stat['FG3M'],
                fg3a=team_stat['FG3A'],
                fg3_pct=team_stat['FG3_PCT'],
                ftm=team_stat['FTM'],
                fta=team_stat['FTA'],
                ft_pct=team_stat['FT_PCT'],
                oreb=team_stat['OREB'],
                dreb=team_stat['DREB'],
                reb=team_stat['REB'],
                ast=team_stat['AST'],
                stl=team_stat['STL'],
                blk=team_stat['BLK'],
                to=team_stat['TO'],
                pf=team_stat['PF'],
                pts=team_stat['PTS'],
                plus_minus=plus_minus,
                status=status
            ))
        log_message(f"Added all objects for game: {game_id}")

        session.commit()
        log_message(f"Committed session for game: {game_id}")

    except Exception as e:
        log_error(f'Error processing file {file_name}: {str(e)}')
