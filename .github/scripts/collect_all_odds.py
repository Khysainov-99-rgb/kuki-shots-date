#!/usr/bin/env python3
import json
import os
import requests
import re
from datetime import datetime

DATA_FILE = "data/all_odds.json"
URL = "https://m.winline.ru/stavki/sport/basketbol"

def fetch_all_odds():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text
        print("Страница загружена")
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return []

    matches = []
    # Ищем блоки с матчами (упрощённый поиск)
    lines = html.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        # Ищем строки, содержащие названия команд (через " – ")
        if ' – ' in line and ('Нью-Йорк' in line or 'Кливленд' in line or 'Майами' in line or 'Атланта' in line or 'Бостон' in line or 'Орландо' in line or 'Детройт' in line or 'Мемфис' in line or 'Сан-Антонио' in line or 'Филадельфия' in line or 'Денвер' in line or 'Портленд' in line or 'Торонто' in line or 'Лейкерс' in line or 'Голден Стэйт' in line or 'Чикаго' in line or 'Милуоки' in line or 'Даллас' in line or 'Хьюстон' in line or 'Финикс' in line or 'Юта' in line or 'Оклахома' in line or 'Сакраменто' in line or 'Клипперс' in line):
            parts = line.split(' – ')
            if len(parts) >= 2:
                home = parts[0].strip()
                away = parts[1].strip()
                # Ищем коэффициенты в следующих строках
                odds_found = []
                for j in range(i+1, min(i+5, len(lines))):
                    odds_line = lines[j].strip()
                    numbers = re.findall(r'\b\d+\.\d{2}\b', odds_line)
                    for num in numbers:
                        try:
                            odds_found.append(float(num))
                        except:
                            pass
                    if len(odds_found) >= 2:
                        break
                if len(odds_found) >= 2:
                    matches.append({
                        "home": home,
                        "away": away,
                        "odds_home": odds_found[0],
                        "odds_away": odds_found[1],
                        "timestamp": datetime.now().isoformat()
                    })
                    print(f"Найден матч: {home} – {away} ({odds_found[0]} / {odds_found[1]})")
    print(f"Всего найдено матчей: {len(matches)}")
    return matches

def save_odds(matches):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
    print(f"Сохранено в {DATA_FILE}")

if __name__ == "__main__":
    matches = fetch_all_odds()
    if matches:
        save_odds(matches)
    else:
        print("Матчей не найдено")
        save_odds([])
