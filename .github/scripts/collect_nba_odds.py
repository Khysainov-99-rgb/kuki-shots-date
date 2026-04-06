#!/usr/bin/env python3
import json
import os
import requests
from datetime import datetime

DATA_FILE = "data/nba_odds.json"
URL = "https://www.livecup.run/basketball/matches/today/"

def fetch_odds():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text
        print("Страница загружена")
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return []

    import re
    matches = []
    pattern = r'<div class="match.*?<div class="homeTeam">(.*?)</div>.*?<div class="awayTeam">(.*?)</div>.*?<span class="odds.*?">(.*?)</span>.*?<span class="odds.*?">(.*?)</span>'
    blocks = re.findall(pattern, html, re.DOTALL)
    
    for home, away, odds_h, odds_a in blocks:
        try:
            odds_home = float(odds_h.replace(',', '.'))
            odds_away = float(odds_a.replace(',', '.'))
        except:
            continue
        matches.append({
            "league": "NBA",
            "home": home.strip(),
            "away": away.strip(),
            "odds_home": odds_home,
            "odds_away": odds_away,
            "timestamp": datetime.now().isoformat()
        })
    print(f"Найдено {len(matches)} матчей")
    return matches

def save_odds(matches):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
    print(f"Сохранено в {DATA_FILE}")

if __name__ == "__main__":
    matches = fetch_odds()
    if matches:
        save_odds(matches)
    else:
        print("Матчей не найдено, создаём пустой файл")
        save_odds([])
