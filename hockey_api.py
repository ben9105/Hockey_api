import json
import requests

api = 'https://statsapi.web.nhl.com/api/v1/teams'
api_team = 'https://statsapi.web.nhl.com/api/v1/teams/4'
game = 'https://statsapi.web.nhl.com/api/v1/game/2019020012/feed/live' #random game going on now to test api



'''
Flyers ID = 4
link /api/v1/teams/4

**need to find a way to pull game date from team name search and return live game from that day**

'''

def print_json(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

response = requests.get(game)
# print(response.status_code)
home_goal = response.json()['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['goals']
away_goal = response.json()['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['goals']

home_name = response.json()['liveData']['boxscore']['teams']['home']['team']['name']
away_name = response.json()['liveData']['boxscore']['teams']['away']['team']['name']

print(f'The score is {away_name}: {away_goal} and {home_name}: {home_goal}.')

print('')

if (home_goal == away_goal):
    print('Tie game!')
elif (home_goal > away_goal):
    print(f'{home_name} are winning!')
else:
    print(f'{away_name} are winning')
