#!/usr/bin/env python3
import json
import os
import re
import requests
from datetime import datetime

# ===== НАСТРОЙКИ =====
MAIN_URL = "https://www.livecup.run/basketball/"   # Главная страница
DATA_FILE = "data/all_bball_odds.json"            # Файл для данных
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_all_match_links():
    """Собирает ссылки на все матчи за сегодня с главной страницы"""
    links = []
    try:
        response = requests.get(MAIN_URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
        html = response.text

        # Ищем все ссылки на матчи (URL содержат '/match/')
        # Пример: /basketball/match/team1-team2-2026.../
        pattern = r'href="(/basketball/match/[^"]+)"'
        matches = re.findall(pattern, html)

        # Преобразуем относительные ссылки в абсолютные
        for match in matches:
            full_url = f"https://www.livecup.run{match}"
            if full_url not in links:
                links.append(full_url)

        print(f"Найдено ссылок на матчи: {len(links)}")
        return links
    except Exception as e:
        print(f"Ошибка при сборе ссылок: {e}")
        return []

def extract_odds_from_match(url):
    """Извлекает коэффициенты со страницы матча"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        html = response.text

        # Извлекаем названия команд из <title> или из страницы
        title_match = re.search(r'<title>(.*?)</title>', html)
        title = title_match.group(1) if title_match else ""

        # Простой поиск пар чисел (коэффициентов) на странице
        odds = re.findall(r'(\d+\.\d{2})', html)
        odds_floats = [float(o) for o in odds if float(o) > 1.0 and float(o) < 10.0]

        # Берём первые два найденных коэффициента (для П1 и П2)
        odds_home = odds_floats[0] if len(odds_floats) > 0 else 0
        odds_away = odds_floats[1] if len(odds_floats) > 1 else 0

        return {
            "match": title,
            "url": url,
            "odds_home": odds_home,
            "odds_away": odds_away,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Ошибка при обработке {url}: {e}")
        return None

def save_odds(all_odds):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_odds, f, ensure_ascii=False, indent=2)
    print(f"Сохранено {len(all_odds)} матчей")

if __name__ == "__main__":
    print("🚀 Начинаем сбор коэффициентов со всех матчей дня...")
    match_links = get_all_match_links()

    if not match_links:
        print("Матчей не найдено.")
        exit(0)

    all_odds = []
    for idx, link in enumerate(match_links, 1):
        print(f"Обработка {idx}/{len(match_links)}: {link}")
        match_data = extract_odds_from_match(link)
        if match_data:
            all_odds.append(match_data)

    save_odds(all_odds)
    print("✅ Готово!")
