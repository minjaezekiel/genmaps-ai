import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import numpy as np
from .knowledge_base import KnowledgeBase

class SurveyManager:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.surveys_dir = Path(__file__).parent.parent / "data" / "user_surveys"
        self.surveys_dir.mkdir(exist_ok=True)
        self.survey_file = self.surveys_dir / "survey_records.json"
        self.surveys = self._load_surveys()

    def _load_surveys(self) -> Dict:
        if not self.survey_file.exists():
            return {"surveys": []}
        with open(self.survey_file, 'r') as f:
            return json.load(f)

    def _save_surveys(self) -> None:
        with open(self.survey_file, 'w') as f:
            json.dump(self.surveys, f, indent=4)

    def create_survey(self, coordinates: List[Dict], formation: str = None) -> str:
        """Create a new survey and return its ID"""
        survey_id = f"survey_{len(self.surveys['surveys']) + 1:03d}"
        new_survey = {
            "id": survey_id,
            "coordinates": coordinates,
            "descriptions": [],
            "formation": formation,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        self.surveys["surveys"].append(new_survey)
        self._save_surveys()
        return survey_id

    def add_description(self, survey_id: str, description: str, location_index: int = 0) -> Optional[Dict]:
        """Add a description to a survey and return inferred type"""
        survey = self._get_survey(survey_id)
        if not survey:
            return None
            
        inferred_type = self.infer_type_from_description(description)
        desc_entry = {
            "location_index": location_index,
            "text": description,
            "inferred_type": inferred_type
        }
        
        survey["descriptions"].append(desc_entry)
        self._save_surveys()
        
        if inferred_type:
            return self._get_type_details(inferred_type)
        return None

    def _get_survey(self, survey_id: str) -> Optional[Dict]:
        for survey in self.surveys["surveys"]:
            if survey["id"] == survey_id:
                return survey
        return None

    def infer_type_from_description(self, description: str) -> Optional[str]:
        """Use NLP to infer rock/mineral type from description"""
        # In a real implementation, this would use a trained NLP model
        description = description.lower()
        
        # Simple keyword matching (would be replaced with ML model)
        if "granite" in description or ("coarse" in description and "feldspar" in description):
            return "Granite"
        elif "basalt" in description or ("fine" in description and "volcanic" in description):
            return "Basalt"
        elif "quartz" in description and "clear" in description:
            return "Quartz"
        elif "limestone" in description or ("reacts" in description and "acid" in description):
            return "Limestone"
        return None

    def _get_type_details(self, type_name: str) -> Dict:
        """Get details for inferred type from knowledge base"""
        mineral = self.knowledge_base.get_mineral(type_name)
        if mineral:
            return {"type": "mineral", "data": mineral}
            
        rock = self.knowledge_base.get_rock(type_name)
        if rock:
            return {"type": "rock", "data": rock}
            
        return {"type": "unknown", "data": {"name": type_name}}

    def get_survey_for_mapping(self, survey_id: str) -> Dict:
        """Prepare survey data for map generation"""
        survey = self._get_survey(survey_id)
        if not survey:
            return None
            
        map_data = {
            "coordinates": survey["coordinates"],
            "units": [],
            "descriptions": []
        }
        
        # Create geological units based on descriptions
        for i, desc in enumerate(survey["descriptions"]):
            if desc["inferred_type"]:
                unit = {
                    "type": desc["inferred_type"],
                    "coordinates": [survey["coordinates"][desc["location_index"]]],
                    "description": desc["text"]
                }
                map_data["units"].append(unit)
                
        return map_data