#!/usr/bin/env python3
import json
import os
import requests
from datetime import datetime

API_KEY = "13437d096508047c74da034c9656ec31"
REGIONS = "eu,us"
MARKETS = "h2h"
ODDS_FORMAT = "decimal"

def fetch_odds(sport_key):
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds"
    params = {
        "apiKey": API_KEY,
        "regions": REGIONS,
        "markets": MARKETS,
        "oddsFormat": ODDS_FORMAT,
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка {sport_key}: {e}")
        return []

def parse_event(event):
    home = event.get('home_team', '')
    away = event.get('away_team', '')
    odds_home = None
    odds_away = None
    for bm in event.get('bookmakers', []):
        for m in bm.get('markets', []):
            if m.get('key') == 'h2h':
                for o in m.get('outcomes', []):
                    if o.get('name') == home:
                        odds_home = o.get('price')
                    elif o.get('name') == away:
                        odds_away = o.get('price')
    return {
        "home": home,
        "away": away,
        "odds_home": odds_home,
        "odds_away": odds_away,
        "time": event.get('commence_time')
    }

def main():
    print(f"Сбор LoL данных: {datetime.now()}")
    
    # Пробуем разные sport_key для LoL
    possible_keys = ["esports", "esports_lol", "lol", "league_of_legends"]
    all_matches = []
    
    for key in possible_keys:
        print(f"Проверяю {key}...")
        data = fetch_odds(key)
        if data:
            print(f"  Найдено {len(data)} матчей в {key}")
            for event in data:
                parsed = parse_event(event)
                if parsed['home'] and parsed['away']:
                    all_matches.append(parsed)
            break
    
    if not all_matches:
        print("❌ Матчи LoL не найдены. Возможно, сегодня нет игр.")
        all_matches = []
    
    output = {
        "timestamp": datetime.now().isoformat(),
        "matches": all_matches
    }
    
    os.makedirs("data", exist_ok=True)
    with open("data/lol_odds.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"✅ Сохранено {len(all_matches)} матчей в data/lol_odds.json")

if __name__ == "__main__":
    main()
