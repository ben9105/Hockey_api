import json
import requests
import smtplib
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

api = 'https://statsapi.web.nhl.com/api/v1/teams'
api_team = 'https://statsapi.web.nhl.com/api/v1/teams/4'
game = 'https://statsapi.web.nhl.com/api/v1/game/2019020012/feed/live' #random game going on now to test api
logo = 'https://records.nhl.com/site/api/franchise?include=teams.id&include=teams.active&include=teams.triCode&include=teams.placeName&include=teams.commonName&include=teams.fullName&include=teams.logos&include=teams.conference.name&include=teams.division.name&include=teams.franchiseTeam.firstSeason.id&include=teams.franchiseTeam.lastSeason.id&include=teams.franchiseTeam.teamCommonName'
flyers_logo = "['15']['teams']['0']['logos']['3']['secureUrl']"

'''
Flyers ID = 4
link /api/v1/teams/4

-------------------

Flyers logo ID = 15
good logo is['15']['teams']['0']['logos']['3']['secureUrl']
'https://assets.nhle.com/logos/nhl/svg/PHI_19671968-19981999_dark.svg'


**need to find a way to pull game date from team name search and return live game from that day**

'''

# logo_response = requests.get(logo)
# print(logo_response.json()[15]['teams'][0]['logos'][3]['secureUrl'])

def print_json(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


# clean this up for function call and global
response = requests.get(game)
# print(response.status_code)
home_goal = response.json()['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['goals']
away_goal = response.json()['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['goals']

home_name = response.json()['liveData']['boxscore']['teams']['home']['team']['name']
away_name = response.json()['liveData']['boxscore']['teams']['away']['team']['name']

def score():
    response = requests.get(game)
    home_goal = response.json()['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['goals']
    away_goal = response.json()['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['goals']

    home_name = response.json()['liveData']['boxscore']['teams']['home']['team']['name']
    away_name = response.json()['liveData']['boxscore']['teams']['away']['team']['name']

    score_text = f'The score is {away_name}: {away_goal} and {home_name}: {home_goal}.'
    return score_text

# print(score())

def who_winning():
    if (home_goal == away_goal):
        return 'Tie game!'
    elif (home_goal > away_goal):
        return f'{home_name} are winning!'
    else:
        return f'{away_name} are winning'

# print(who_winning())

def send_mail():
    try:
        message = MIMEMultipart()
        message['Subject'] = 'Hockey score'
        message['From'] = 'EMAIL'
        message['To'] = 'EMAIL'
        username = 'USERNAME_GMAIL.COM'
        password = 'PASSWORD'

        message.attach(MIMEText(score()))
        message.attach(MIMEText('\r\n\n'))
        message.attach(MIMEText(who_winning()))

        smtp = smtplib.SMTP('smtp.gmail.com', 587, timeout=120)
        smtp.starttls()
        # smtp.ehlo()

        smtp.login(username, password)
        smtp.sendmail(message['From'], message['To'], message.as_string())

        print('Email sent')
    except Exception as e:
        print(e)
    finally:
        smtp.quit()


send_mail()

