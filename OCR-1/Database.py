import pandas as pd
from nba_api.stats.static import players

def fullnames():
    full_names = []
    all_players = players.get_players()
    for player in all_players:
        full_names.append(' ' + player['full_name'])
    return full_names

def firstnames():
    first_names = []
    all_players = players.get_players()
    for player in all_players:
        first_names.append(' ' + player['first_name'])
    return first_names

def lastnames():
    last_names = []
    all_players = players.get_players()
    for player in all_players:
        last_names.append(' ' + player['last_name'])
    return last_names

def abbreviatednames():
    abbreviated_names = []
    all_players = players.get_players()
    for player in all_players:
        abbreviated_names.append(player['first_name'][:1] + '. ' + player['last_name'])
    return abbreviated_names

df = pd.DataFrame(fullnames(), columns=['Full Name'])
df.loc[:,"First Name"]=firstnames()
df.loc[:,"Last Name"]=lastnames()
df.loc[:,"First Name Initial with Full Last Name"]=abbreviatednames()
print(df)
df.to_csv('Database.csv')

abbreviated_names=str(abbreviatednames())
names=[]
