import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from pathlib import Path
import json
from core.knowledge_base import KnowledgeBase

class OnlineLearner:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.sources = [
            "https://en.wikipedia.org/wiki/List_of_minerals",
            "https://en.wikipedia.org/wiki/List_of_rock_types",
            "https://www.mindat.org/"
        ]

    def update_knowledge_base(self) -> None:
        """Fetch new data from online sources and update knowledge base"""
        new_minerals = self._scrape_mineral_data()
        new_rocks = self._scrape_rock_data()
        
        for mineral in new_minerals:
            self.knowledge_base.add_mineral(mineral)
            
        for rock in new_rocks:
            self.knowledge_base.add_rock(rock)

    def _scrape_mineral_data(self) -> List[Dict]:
        """Scrape mineral data from online sources"""
        minerals = []
        try:
            response = requests.get(self.sources[0])
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # This is a simplified example - real implementation would parse tables
            tables = soup.find_all('table', {'class': 'wikitable'})
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip header
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        mineral = {
                            "name": cols[0].text.strip(),
                            "description": cols[1].text.strip()
                        }
                        minerals.append(mineral)
        except Exception as e:
            print(f"Error scraping mineral data: {e}")
        return minerals

    def _scrape_rock_data(self) -> List[Dict]:
        """Scrape rock data from online sources"""
        rocks = []
        try:
            response = requests.get(self.sources[1])
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # This is a simplified example - real implementation would parse tables
            tables = soup.find_all('table', {'class': 'wikitable'})
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip header
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        rock = {
                            "name": cols[0].text.strip(),
                            "type": cols[1].text.strip() if len(cols) > 1 else "",
                            "description": cols[2].text.strip() if len(cols) > 2 else ""
                        }
                        rocks.append(rock)
        except Exception as e:
            print(f"Error scraping rock data: {e}")
        return rocks