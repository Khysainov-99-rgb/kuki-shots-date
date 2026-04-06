#!/usr/bin/env python3
import json
import os
import requests
from datetime import datetime

# === НАСТРОЙКИ ===
API_KEY = "13437d096508047c74da034c9656ec31"
REGIONS = "us,eu"                     # Регионы букмекеров
MARKETS = "h2h,spreads,totals"        # Рынки: исходы, форы, тоталы
ODDS_FORMAT = "decimal"               # Формат коэффициентов

# === ФУНКЦИЯ: ПОЛУЧИТЬ СПИСОК ДОСТУПНЫХ ЛИГ ===
def get_available_basketball_leagues():
    """Запрашивает у API список всех поддерживаемых видов спорта и отбирает баскетбольные лиги"""
    url = f"https://api.the-odds-api.com/v4/sports?apiKey={API_KEY}"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        sports = response.json()
        
        basketball_leagues = []
        for sport in sports:
            key = sport['key']
            title = sport['title']
            if 'basketball' in key.lower():
                basketball_leagues.append({'key': key, 'title': title})
                print(f"  Найдена лига: {key} - {title}")
        return basketball_leagues
    except Exception as e:
        print(f"❌ Ошибка при получении списка лиг: {e}")
        return []

# === ФУНКЦИЯ: ПОЛУЧИТЬ КОЭФФИЦИЕНТЫ ДЛЯ ОДНОЙ ЛИГИ ===
def fetch_league_odds(league_key):
    """Получает коэффициенты для конкретной лиги по её sport_key"""
    url = f"https://api.the-odds-api.com/v4/sports/{league_key}/odds"
    params = {
        "apiKey": API_KEY,
        "regions": REGIONS,
        "markets": MARKETS,
        "oddsFormat": ODDS_FORMAT,
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        print(f"  {league_key}: {len(data)} матчей")
        return data
    except Exception as e:
        print(f"  {league_key}: ошибка - {e}")
        return []

# === ОСНОВНАЯ ФУНКЦИЯ ===
def main():
    print(f"\n{'='*50}")
    print(f"СБОР ДАННЫХ НАЧАТ: {datetime.now()}")
    print('='*50)
    
    # 1. Получаем актуальный список баскетбольных лиг
    print("\n1. Запрашиваю список доступных баскетбольных лиг...")
    basketball_leagues = get_available_basketball_leagues()
    
    if not basketball_leagues:
        print("❌ Не удалось получить список лиг. Проверьте API ключ и интернет-соединение.")
        return
    
    print(f"\n✅ Найдено баскетбольных лиг: {len(basketball_leagues)}")
    
    # 2. Собираем коэффициенты для каждой лиги
    print("\n2. Собираю коэффициенты...")
    all_data = {}
    total_matches = 0
    
    for league in basketball_leagues:
        league_key = league['key']
        odds_data = fetch_league_odds(league_key)
        if odds_data:
            all_data[league_key] = odds_data
            total_matches += len(odds_data)
    
    # 3. Сохраняем результат
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "total_matches": total_matches,
        "leagues": all_data
    }
    
    os.makedirs("data", exist_ok=True)
    with open("data/basketball_odds.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*50}")
    print(f"✅ СБОР ЗАВЕРШЁН. СОХРАНЕНО МАТЧЕЙ: {total_matches}")
    print(f"📁 Файл: data/basketball_odds.json")
    print('='*50)

if __name__ == "__main__":
    main()
