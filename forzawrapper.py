import pandas as pd
import numpy as np
import requests 

def get_qualifying():
    response = requests.get("https://forzafootball.com/sv/api/tournament/429/tables").json()
    qualifying = []
    for group in response['tables']:
        qualifying += [team['team']['name'] for team in group['rows']][:2]
    return pd.DataFrame(qualifying)


def get_scores():
    """
    get_scores makes request to forza API and gets finished results and live results
    """
    info = {}
    response = requests.get("https://forzafootball.com/en-GB/api/tournament/429").json()
    matcher = response['matches']
    games = []
    scores = []
    times = []
    groups = []
    for match in matcher:
        if match['status'] != 'before':
            home_team = match['home_team']['name']
            away_team = match['away_team']['name']
            groups.append(match['series'])
            time = match['kickoff_at']
            #info[f'{home_team} vs {away_team}'] = match['score']['current'] #Tror om det blir samma lag(key) skrivs resultatet från den matchen över
            games.append(f'{home_team} vs {away_team}')
            scores.append('-'.join([str(x) for x in match['score']['current']]))
            times.append(time)
        else:
            home_team = match['home_team']['name']
            away_team = match['away_team']['name']
            time = match['kickoff_at']
            groups.append(match['series'])
            games.append(f'{home_team} vs {away_team}')
            scores.append(None)
            times.append(time)
    return pd.DataFrame(list(zip(times, games, scores, groups)), columns=["Kickoff", "Teams", "Score", "Group"]).sort_values("Kickoff").reset_index(drop=True)
    #return pd.DataFrame(info)

def main():
    print(get_scores())
    print(get_qualifying())

if __name__ == "__main__":
    main()