#!/usr/bin/env python3
import json
import os
import requests
from datetime import datetime

# === НАСТРОЙКИ ===
API_KEY = "e9597efb-d956-41d1-b36b-8aa4d1f63dc9"
BASE_URL = "https://api.balldontlie.io/v1"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

# === ФУНКЦИЯ: ПОЛУЧИТЬ ПРЕДСТОЯЩИЕ МАТЧИ LoL ===
def get_upcoming_matches():
    """Получает предстоящие матчи по League of Legends"""
    url = f"{BASE_URL}/lol/games"
    params = {
        "per_page": 50,
        "start_date": datetime.now().strftime("%Y-%m-%d")
    }
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=15)
        response.raise_for_status()
        return response.json().get('data', [])
    except Exception as e:
        print(f"❌ Ошибка получения матчей: {e}")
        return []

# === ФУНКЦИЯ: ПОЛУЧИТЬ КОЭФФИЦИЕНТЫ ДЛЯ МАТЧА ===
def get_match_odds(game_id):
    """Получает коэффициенты для конкретного матча"""
    url = f"{BASE_URL}/lol/odds"
    params = {"game_ids[]": game_id}
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get('data', [])
    except Exception as e:
        return []

# === ОСНОВНАЯ ФУНКЦИЯ ===
def main():
    print(f"\n{'='*50}")
    print(f"СБОР ДАННЫХ LoL НАЧАТ: {datetime.now()}")
    print('='*50)
    
    # 1. Получаем предстоящие матчи
    print("\n1. Запрашиваю предстоящие матчи LoL...")
    matches = get_upcoming_matches()
    
    if not matches:
        print("❌ Нет предстоящих матчей или ошибка подключения.")
        print("   Проверьте API ключ и интернет-соединение.")
        return
    
    print(f"✅ Найдено матчей: {len(matches)}")
    
    # 2. Для каждого матча получаем коэффициенты
    print("\n2. Собираю коэффициенты...")
    matches_with_odds = []
    
    for game in matches:
        game_id = game.get('id')
        home = game.get('home_team', {}).get('name', '')
        away = game.get('visitor_team', {}).get('name', '')
        start_time = game.get('start_date', '')
        league = game.get('league', {}).get('name', 'Unknown')
        
        print(f"  Обработка: {league} - {home} vs {away}")
        
        odds_data = get_match_odds(game_id)
        
        odds_home = None
        odds_away = None
        
        for odd in odds_data:
            # Ищем moneyline (исход матча)
            if odd.get('type') == 'moneyline':
                for price in odd.get('prices', []):
                    if price.get('team_name') == home:
                        odds_home = price.get('price')
                    elif price.get('team_name') == away:
                        odds_away = price.get('price')
        
        match_info = {
            "id": game_id,
            "league": league,
            "home": home,
            "away": away,
            "odds_home": odds_home,
            "odds_away": odds_away,
            "time": start_time,
            "status": game.get('status')
        }
        
        if match_info['home'] and match_info['away']:
            matches_with_odds.append(match_info)
    
    # 3. Сохраняем результат
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "total_matches": len(matches_with_odds),
        "matches": matches_with_odds
    }
    
    os.makedirs("data", exist_ok=True)
    with open("data/lol_odds.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*50}")
    print(f"✅ СБОР ЗАВЕРШЁН. СОХРАНЕНО МАТЧЕЙ: {len(matches_with_odds)}")
    print(f"📁 Файл: data/lol_odds.json")
    print('='*50)

if __name__ == "__main__":
    main()
