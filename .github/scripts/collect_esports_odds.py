#!/usr/bin/env python3
import json
import os
import re
import requests
from datetime import datetime

def fetch_parimatch_esports():
    """Парсит коэффициенты на киберспорт с Parimatch.ru"""
    
    url = "https://winline.ru/esports/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")
        return []
    
    # Ищем блоки с матчами
    matches = []
    
    # Шаблон для поиска матчей (адаптирован под Parimatch)
    # Пример: <div class="event-row">Team A vs Team B</div>
    pattern = r'<div class="event-row[^"]*">.*?<span class="team-name[^"]*">([^<]+)</span>.*?<span class="team-name[^"]*">([^<]+)</span>.*?<span class="odds-value[^"]*">([\d\.]+)</span>.*?<span class="odds-value[^"]*">([\d\.]+)</span>'
    
    blocks = re.findall(pattern, html, re.DOTALL)
    
    for home, away, odds_home, odds_away in blocks:
        matches.append({
            "home": home.strip(),
            "away": away.strip(),
            "odds_home": float(odds_home),
            "odds_away": float(odds_away),
            "league": "CS2/LoL/Dota2",
            "timestamp": datetime.now().isoformat()
        })
    
    return matches

def main():
    print(f"Сбор данных начат: {datetime.now()}")
    matches = fetch_parimatch_esports()
    
    os.makedirs("data", exist_ok=True)
    with open("data/esports_odds.json", "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Сохранено матчей: {len(matches)}")

if __name__ == "__main__":
    main()
