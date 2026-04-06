#!/usr/bin/env python3
import json
import os
import requests
import logging
from datetime import datetime

# Создаём папку для логов, если её нет
os.makedirs('logs', exist_ok=True)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/nba_odds_collector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('nba_odds_collector')

DATA_FILE = "data/nba_odds.json"
URL = "https://www.livecup.run/basketball/matches/today/"

def fetch_odds():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text
        logger.info("Страница загружена")
    except Exception as e:
        logger.error(f"Ошибка загрузки: {e}")
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
    logger.info(f"Найдено {len(matches)} матчей")
    return matches

def save_odds(matches):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
    logger.info(f"Сохранено в {DATA_FILE}")

if __name__ == "__main__":
    matches = fetch_odds()
    if matches:
        save_odds(matches)
    else:
        logger.warning("Матчей не найдено, создаём пустой файл")
        save_odds([])
