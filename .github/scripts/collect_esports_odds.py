#!/usr/bin/env python3
import json
import os
import re
import requests
from datetime import datetime

def fetch_hltv_matches():
    """Парсит матчи и коэффициенты с HLTV.org (только CS2)"""
    
    url = "https://www.hltv.org/matches"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text
        
        # Сохраняем для отладки
        os.makedirs("data", exist_ok=True)
        with open("data/debug.html", "w", encoding="utf-8") as f:
            f.write(html)
        
        # Ищем матчи
        matches = []
        
        # Шаблон для поиска матчей
        pattern = r'<div class="match">.*?<div class="team1">.*?<div class="name">([^<]+)</div>.*?<div class="team2">.*?<div class="name">([^<]+)</div>'
        
        found = re.findall(pattern, html, re.DOTALL)
        
        for home, away in found:
            matches.append({
                "home": home.strip(),
                "away": away.strip(),
                "odds_home": None,
                "odds_away": None,
                "league": "CS2",
                "timestamp": datetime.now().isoformat()
            })
        
        print(f"✅ Найдено матчей: {len(matches)}")
        return matches
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return []

def main():
    print(f"Сбор данных начат: {datetime.now()}")
    matches = fetch_hltv_matches()
    
    os.makedirs("data", exist_ok=True)
    with open("data/esports_odds.json", "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Сохранено матчей: {len(matches)}")

if __name__ == "__main__":
    main()
