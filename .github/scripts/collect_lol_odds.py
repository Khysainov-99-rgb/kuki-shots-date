#!/usr/bin/env python3
import json
import os
import requests
from datetime import datetime

# === НАСТРОЙКИ ===
API_KEY = "yiTEg6rwQfJBQ7iHr4BWhJzSs_1WqS4HxxiL1nRAlU5gYoxk9EM"
BASE_URL = "https://api.pandascore.co"

HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# === ФУНКЦИЯ: ПОЛУЧИТЬ ПРЕДСТОЯЩИЕ МАТЧИ LoL ===
def get_upcoming_matches():
    """Получает предстоящие матчи по League of Legends"""
    url = f"{BASE_URL}/lol/matches/upcoming"
    params = {
        "per_page": 50,
        "sort": "begin_at"
    }
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Ошибка получения матчей: {e}")
        return []

# === ФУНКЦИЯ: ПОЛУЧИТЬ КОЭФФИЦИЕНТЫ ДЛЯ МАТЧА ===
def get_match_odds(match_id):
    """Получает коэффициенты для конкретного матча"""
    url = f"{BASE_URL}/lol/matches/{match_id}/odds"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"  ⚠️ Нет коэффициентов для матча {match_id}: {e}")
        return []

# === ОСНОВНАЯ ФУНКЦИЯ ===
def main():
    print(f"\n{'='*50}")
    print(f"СБОР ДАННЫХ LoL (PandaScore) НАЧАТ: {datetime.now()}")
    print('='*50)
    
    # 1. Получаем предстоящие матчи
    print("\n1. Запрашиваю предстоящие матчи LoL...")
    matches = get_upcoming_matches()
    
    if not matches:
        print("❌ Нет предстоящих матчей или ошибка подключения.")
        return
    
    print(f"✅ Найдено матчей: {len(matches)}")
    
    # 2. Для каждого матча получаем коэффициенты
    print("\n2. Собираю коэффициенты...")
    matches_with_odds = []
    
    for match in matches:
        match_id = match.get('id')
        name = f"{match.get('name', '')}"
        league = match.get('league', {}).get('name', 'Unknown')
        begin_at = match.get('begin_at', '')
        
        print(f"  Обработка: {league} - {name}")
        
        odds_data = get_match_odds(match_id)
        
        # Извлекаем коэффициенты на исход (Moneyline)
        odds_home = None
        odds_away = None
        
        for odd in odds_data:
            if odd.get('name') == 'moneyline':
                for outcome in odd.get('odds', []):
                    if outcome.get('name') == match.get('opponents', [{}])[0].get('name'):
                        odds_home = outcome.get('value')
                    elif len(match.get('opponents', [])) > 1 and outcome.get('name') == match.get('opponents', [{}])[1].get('name'):
                        odds_away = outcome.get('value')
        
        match_info = {
            "id": match_id,
            "league": league,
            "home": match.get('opponents', [{}])[0].get('name') if match.get('opponents') else None,
            "away": match.get('opponents', [{}])[1].get('name') if len(match.get('opponents', [])) > 1 else None,
            "odds_home": odds_home,
            "odds_away": odds_away,
            "time": begin_at,
            "status": match.get('status'),
            "tournament": match.get('tournament', {}).get('name')
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
