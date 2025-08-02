import json
from pathlib import Path
from typing import Dict, List, Optional

class KnowledgeBase:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.minerals = self._load_data("minerals.json")
        self.rocks = self._load_data("rocks.json")
        self.formations = self._load_data("geological_formations.json")

    def _load_data(self, filename: str) -> Dict:
        with open(self.data_dir / filename, 'r') as f:
            return json.load(f)

    def get_mineral(self, name: str) -> Optional[Dict]:
        for mineral in self.minerals.get("minerals", []):
            if mineral["name"].lower() == name.lower():
                return mineral
        return None

    def get_rock(self, name: str) -> Optional[Dict]:
        for rock in self.rocks.get("rocks", []):
            if rock["name"].lower() == name.lower():
                return rock
        return None

    def search_by_property(self, property_name: str, value: str, search_type: str = "mineral") -> List[Dict]:
        results = []
        search_data = self.minerals if search_type == "mineral" else self.rocks
        key = "minerals" if search_type == "mineral" else "rocks"
        
        for item in search_data.get(key, []):
            if property_name in item and str(value).lower() in str(item[property_name]).lower():
                results.append(item)
        return results

    def add_mineral(self, mineral_data: Dict) -> None:
        self.minerals["minerals"].append(mineral_data)
        self._save_data("minerals.json", self.minerals)

    def add_rock(self, rock_data: Dict) -> None:
        self.rocks["rocks"].append(rock_data)
        self._save_data("rocks.json", self.rocks)

    def _save_data(self, filename: str, data: Dict) -> None:
        with open(self.data_dir / filename, 'w') as f:
            json.dump(data, f, indent=4)