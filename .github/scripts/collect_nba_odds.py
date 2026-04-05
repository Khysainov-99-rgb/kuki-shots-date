#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Парсер коэффициентов НБА с сайта Livecup.run
Версия: 1.0
"""

import json
import os
import sys
import logging
import re
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/nba_odds_collector.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('nba_odds_collector')

class NBAAoddsCollector:
    """Сборщик коэффициентов НБА с Livecup.run"""
    
    def __init__(self):
        self.data_dir = 'data/nba'
        self.odds_file = 'data/nba_odds.json'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        }
        self.ensure_directories()
    
    def ensure_directories(self):
        """Создание необходимых директорий"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        logger.info(f"Директории созданы")
    
    def fetch_html(self, url: str) -> Optional[str]:
        """Получение HTML-кода страницы"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            response.encoding = 'utf-8'
            logger.info(f"Загружена страница: {url}")
            return response.text
        except Exception as e:
            logger.error(f"Ошибка загрузки {url}: {e}")
            return None
    
    def parse_nba_odds(self, html: str) -> List[Dict[str, Any]]:
        """
        Парсинг коэффициентов НБА из HTML
        Это упрощённая версия, требующая доработки под реальную структуру страницы
        """
        matches = []
        
        # Ищем блоки с матчами
        # Реальная структура страницы сложнее, этот код нужно адаптировать
        match_blocks = re.findall(r'<div class="match".*?</div>', html, re.DOTALL)
        
        for block in match_blocks:
            # Извлекаем названия команд
            home_match = re.search(r'<div class="homeTeam">(.*?)</div>', block)
            away_match = re.search(r'<div class="awayTeam">(.*?)</div>', block)
            
            if not home_match or not away_match:
                continue
            
            home = home_match.group(1).strip()
            away = away_match.group(1).strip()
            
            # Извлекаем коэффициенты
            odds_home_match = re.search(r'<span class="odds homeOdds">(.*?)</span>', block)
            odds_away_match = re.search(r'<span class="odds awayOdds">(.*?)</span>', block)
            
            if not odds_home_match or not odds_away_match:
                continue
            
            try:
                odds_home = float(odds_home_match.group(1).replace(',', '.'))
                odds_away = float(odds_away_match.group(1).replace(',', '.'))
            except ValueError:
                continue
            
            matches.append({
                "league": "NBA",
                "home": home,
                "away": away,
                "odds_home": odds_home,
                "odds_away": odds_away,
                "source": "livecup.run",
                "timestamp": datetime.now().isoformat()
            })
        
        return matches
    
    def collect_odds(self) -> List[Dict[str, Any]]:
        """Основной метод сбора коэффициентов"""
        # URL страницы с баскетбольными матчами на сегодня
        url = "https://www.livecup.run/basketball/matches/today/"
        
        html = self.fetch_html(url)
        if not html:
            logger.error("Не удалось загрузить страницу")
            return []
        
        matches = self.parse_nba_odds(html)
        logger.info(f"Собрано коэффициентов для {len(matches)} матчей")
        
        # Сохраняем в файл
        if matches:
            with open(self.odds_file, 'w', encoding='utf-8') as f:
                json.dump(matches, f, ensure_ascii=False, indent=2)
            logger.info(f"Сохранено в {self.odds_file}")
        
        return matches
    
    def run(self):
        """Запуск сбора данных"""
        try:
            logger.info("=" * 50)
            logger.info("ЗАПУСК СБОРА КОЭФФИЦИЕНТОВ НБА")
            logger.info("=" * 50)
            
            matches = self.collect_odds()
            
            if not matches:
                logger.warning("Нет данных для обработки")
                return 0
            
            logger.info("✅ Сбор коэффициентов НБА успешно завершён")
            return 0
            
        except Exception as e:
            logger.error(f"❌ Критическая ошибка: {e}")
            return 1

def main():
    collector = NBAAoddsCollector()
    sys.exit(collector.run())

if __name__ == "__main__":
    main()
