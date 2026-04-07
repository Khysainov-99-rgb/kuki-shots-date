#!/usr/bin/env python3
import json
import os
import re
import requests
from datetime import datetime

def fetch_cybersport_odds():
    """Парсит коэффициенты на киберспорт (LoL, CS2, Dota 2) с российского сайта"""
    
    # Можно использовать parimatch.ru или другой российский сайт
    url = "https://www.parimatch.ru/esports/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text
        print("✅ Страница загружена")
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")
        return []
    
    # Парсим названия команд и коэффициенты
    matches = []
    
    # Шаблон для поиска матчей (адаптируется под сайт)
    # Ищем блоки с командами и коэффициентами
    patterns = [
        # Шаблон для формата: Team A vs Team B
        r'([А-Яа-яA-Za-z0-9\s]+)\s+[vV][sS]\s+([А-Яа-яA-Za-z0-9\s]+).*?(\d+\.\d+).*?(\d+\.\d+)',
        # Альтернативный шаблон
        r'"home":"([^"]+)".*?"away":"([^"]+)".*?"price":(\d+\.\d+).*?"price":(\d+\.\d+)',
    ]
    
    for pattern in patterns:
        found = re.findall(pattern, html, re.DOTALL)
        if found:
            for match in found:
                if len(match) >= 4:
                    home = match[0].strip()
                    away = match[1].strip()
                    odds_home = float(match[2])
                    odds_away = float(match[3])
                    
                    matches.append({
                        "home": home,
                        "away": away,
                        "odds_home": odds_home,
                        "odds_away": odds_away,
                        "league": "LoL/CS2/Dota2",
                        "timestamp": datetime.now().isoformat()
                    })
            break
    
    # Если ничего не нашли, сохраняем HTML для анализа
    if not matches:
        os.makedirs("data", exist_ok=True)
        with open("data/debug.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("⚠️ Матчи не найдены. HTML сохранён в data/debug.html")
    else:
        print(f"✅ Найдено матчей: {len(matches)}")
    
    return matches

def main():
    print(f"\n{'='*50}")
    print(f"СБОР ДАННЫХ LoL/КИБЕРСПОРТ НАЧАТ: {datetime.now()}")
    print('='*50)
    
    matches = fetch_cybersport_odds()
    
    os.makedirs("data", exist_ok=True)
    with open("data/lol_odds.json", "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
    
    print(f"📁 Сохранено в data/lol_odds.json")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    main()
