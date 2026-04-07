#!/usr/bin/env python3
import json
import os
import requests
from datetime import datetime

# Бесплатный API без регистрации
API_URL = "https://odds-api.io/api/v1/events"
SPORT = "esports"

def fetch_esports_odds():
    """Получает коэффициенты через бесплатный API odds-api.io"""
    
    params = {
        "sport": SPORT,
        "bookmaker": "pinnacle",
        "limit": 50
    }
    
    try:
        response = requests.get(API_URL, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Найдено матчей: {len(data)}")
            return data
        else:
            print(f"⚠️ API вернул статус: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return []

def main():
    print(f"Сбор данных начат: {datetime.now()}")
    matches = fetch_esports_odds()
    
    os.makedirs("data", exist_ok=True)
    with open("data/esports_odds.json", "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Сохранено матчей: {len(matches)}")

if __name__ == "__main__":
    main()
