#!/usr/bin/env python3
import json
import os
import requests
from datetime import datetime

# === НАСТРОЙКИ ===
# Здесь нужно будет указать URL страницы с коэффициентами
# Например, для HLTV.org (CS2) или Oddspedia
URL = "https://www.hltv.org/matches"  # ВРЕМЕННО

def fetch_odds():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text
        print("✅ Страница загружена")
        return html
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def main():
    print(f"Сбор данных начат: {datetime.now()}")
    html = fetch_odds()
    
    if html:
        # Сохраняем HTML для анализа (временно)
        os.makedirs("data", exist_ok=True)
        with open("data/page.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("✅ HTML сохранён в data/page.html")
    else:
        print("❌ Не удалось загрузить страницу")

if __name__ == "__main__":
    main()
