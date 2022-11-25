import pandas as pd
import numpy as np
import requests 

def big_dick_few_lines():
    response = requests.get("https://forzafootball.com/en-GB/api/tournament/429").json()
    matcher = response['matches']
    data = [(m['kickoff_at'], m['home_team']['name']+" vs "+m['away_team']['name'], '-'.join([str(x) for x in m['score']['current']])) for m in matcher if m['status'] != 'before']
    return pd.DataFrame(data, columns=["Kickoff", "Teams", "Score"]).sort_values("Kickoff")

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
    for match in matcher:
        if match['status'] != 'before':
            home_team = match['home_team']['name']
            away_team = match['away_team']['name']
            time = match['kickoff_at']
            #info[f'{home_team} vs {away_team}'] = match['score']['current'] #Tror om det blir samma lag(key) skrivs resultatet från den matchen över
            games.append(f'{home_team} vs {away_team}')
            scores.append('-'.join([str(x) for x in match['score']['current']]))
            times.append(time)
        else:
            home_team = match['home_team']['name']
            away_team = match['away_team']['name']
            time = match['kickoff_at']
            games.append(f'{home_team} vs {away_team}')
            scores.append(None)
            times.append(time)
    return pd.DataFrame(list(zip(times, games, scores)), columns=["Kickoff", "Teams", "Score"]).sort_values("Kickoff").reset_index(drop=True)
    #return pd.DataFrame(info)

def main():
    print(get_scores())
    print(big_dick_few_lines())

if __name__ == "__main__":
    main()