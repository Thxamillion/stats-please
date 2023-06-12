from nba_api.stats.endpoints import leaguegamefinder
# from nba_api.stats.endpoints import boxscoretraditionalv2
# import time
# import json

# class APIClient:
#     def __init__(self, league_id):
#         self.league_id = league_id

#     def get_game_ids(self):
#         gamefinder = leaguegamefinder.LeagueGameFinder(league_id_nullable=self.league_id)
#         games_dict = gamefinder.get_normalized_dict()
#         games = games_dict['LeagueGameFinderResults']
#         return [game['GAME_ID'] for game in games]

#     def get_game_data(self, game_id):
#         boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
#         return boxscore.get_normalized_dict()

#     def create_game_json_files(self, delay=1):
#         game_ids = self.get_game_ids()

#         for game_id in game_ids:
#             try:
#                 game_data = self.get_game_data(game_id)
#                 with open(f'game_{game_id}.json', 'w') as json_file:
#                     json.dump(game_data, json_file, indent=4)
#                 print(f"Successfully created JSON file for game ID {game_id}")

#                 # Introduce a delay between requests
#                 time.sleep(delay)
#             except Exception as e:
#                 print(f"Failed to create JSON file for game ID {game_id}: {str(e)}")

# # Usage:
# client = APIClient('00')  # Replace '00' with the LeagueID for the 2023 season





from nba_api.stats.endpoints import boxscoresummaryv2, leaguegamefinder
import time
import os
import json
from datetime import datetime

class NBAClient:
    def __init__(self, league_id):
        self.league_id = league_id
        self.error_log = 'error.txt'

    def get_game_ids(self):
        gamefinder = leaguegamefinder.LeagueGameFinder(league_id_nullable=self.league_id)
        games_dict = gamefinder.get_normalized_dict()
        games = games_dict['LeagueGameFinderResults']
        return [game['GAME_ID'] for game in games]

    def get_game_dates_and_officials(self, game_id):
        try:
            boxscore = boxscoresummaryv2.BoxScoreSummaryV2(game_id)
            game_summary = boxscore.get_data_frames()[4]
            officials = boxscore.get_data_frames()[2]
            # with open('1test.txt', 'w') as file:
            #     file.write(str(officials))


            
            
            
            
            game_date = game_summary['GAME_DATE'].values[0]
            officials = [{"OFFICIAL_ID": row[0], "FIRST_NAME": row[1], "LAST_NAME": row[2], "JERSEY_NUM": row[3].strip()} for row in officials.values]

           
            return game_date, officials
        except Exception as e:
            with open(self.error_log, 'a') as error_file:
                error_file.write(f"Error processing game ID {game_id} at {datetime.now()}: {str(e)}\n")
            print(f"Error processing game ID {game_id}: {str(e)}")
            return None, None

    def update_game_json_file(self, delay = 1):
        game_ids = self.get_game_ids()
        for game_id in game_ids:

            game_date, officials = self.get_game_dates_and_officials(game_id)
            if game_date is not None and officials is not None:
                json_file_path = f'game_{game_id}.json'
                if os.path.exists(json_file_path):
                    with open(json_file_path, 'r+') as file:
                        data = json.load(file)
                        data['GAME_DATE'] = game_date
                        data['OFFICIALS'] = officials
                        file.seek(0)
                        json.dump(data, file, indent=4)
                        file.truncate()
                        print(f"Updated file: {json_file_path}")
                else:
                    with open(self.error_log, 'a') as error_file:
                        error_file.write(f"Error processing game ID {game_id} at {datetime.now()}:")
                    print(f"Error processing game ID {game_id} file doesnt exist: ")
            time.sleep(delay)
if __name__ == "__main__":
    client = NBAClient('00')  
    client.update_game_json_file(delay=.9) 

