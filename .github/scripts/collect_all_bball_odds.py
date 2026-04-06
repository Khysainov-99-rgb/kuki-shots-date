#!/usr/bin/env python3
import json
import os
import requests
from datetime import datetime

# ==========================================
# НАСТРОЙКИ
# ==========================================
API_KEY = "13437d096508047c74da034c9656ec31"
REGIONS = "us,eu"
MARKETS = "h2h,spreads,totals"
ODDS_FORMAT = "decimal"

# Все баскетбольные лиги, доступные через The Odds API
BASKETBALL_LEAGUES = [
    "basketball_nba",
    "basketball_ncaab",
    "basketball_wnba",
    "basketball_euroleague",
    "basketball_spain_acb",
    "basketball_germany_bb",
    "basketball_france_lnb",
    "basketball_italy_seriea",
    "basketball_turkey_superl",
    "basketball_greece_a1",
    "basketball_australia_nbl",
    "basketball_china_cba",
]

# ==========================================
# ФУНКЦИИ
# ==========================================
def fetch_league(league_key):
    """Получает коэффициенты для одной лиги"""
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
        print(f"{league_key}: {len(data)} матчей")
        return data
    except Exception as e:
        print(f"{league_key}: ошибка - {e}")
        return []

def save_odds(all_data):
    """Сохраняет данные в JSON файл"""
    os.makedirs("data", exist_ok=True)
    with open("data/basketball_odds.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print("Данные сохранены в data/basketball_odds.json")

# ==========================================
# ГЛАВНАЯ ФУНКЦИЯ
# ==========================================
def main():
    print(f"Сбор данных начат: {datetime.now()}")
    print("=" * 50)
    
    all_data = {}
    for league in BASKETBALL_LEAGUES:
        all_data[league] = fetch_league(league)
    
    save_odds(all_data)
    print("=" * 50)
    print("Сбор данных завершён.")

if __name__ == "__main__":
    main()
