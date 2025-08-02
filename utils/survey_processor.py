import numpy as np
from typing import Dict, List
from core.knowledge_base import KnowledgeBase

class SurveyProcessor:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()

    def process_survey_data(self, survey_data: Dict) -> Dict:
        """Process raw survey data into structured geological information"""
        processed = {
            "units": self._identify_units(survey_data),
            "boundaries": self._identify_boundaries(survey_data),
            "structural_features": self._identify_structural_features(survey_data),
            "coordinates": survey_data.get("coordinates", [])
        }
        return processed

    def _identify_units(self, survey_data: Dict) -> List[Dict]:
        """Identify and characterize geological units"""
        units = []
        for unit in survey_data.get("units", []):
            detailed_info = self._get_unit_details(unit["type"])
            units.append({
                "type": unit["type"],
                "coordinates": unit["coordinates"],
                "properties": detailed_info,
                "description": unit.get("description", "")
            })
        return units

    def _get_unit_details(self, unit_type: str) -> Dict:
        """Get detailed information about a geological unit"""
        rock = self.knowledge_base.get_rock(unit_type)
        if rock:
            return {"classification": "rock", "data": rock}
            
        mineral = self.knowledge_base.get_mineral(unit_type)
        if mineral:
            return {"classification": "mineral", "data": mineral}
            
        return {"classification": "unknown", "data": {"name": unit_type}}

    def _identify_boundaries(self, survey_data: Dict) -> List[Dict]:
        """Identify boundaries between different units"""
        boundaries = []
        units = survey_data.get("units", [])
        
        if len(units) > 1:
            for i in range(len(units)-1):
                boundary = {
                    "type": "contact",
                    "between": [units[i]["type"], units[i+1]["type"]],
                    "coordinates": self._interpolate_points(
                        units[i]["coordinates"][-1],
                        units[i+1]["coordinates"][0]
                    )
                }
                boundaries.append(boundary)
                
        return boundaries

    def _interpolate_points(self, point1: Dict, point2: Dict, n_points: int = 5) -> List[Dict]:
        """Interpolate between two coordinate points"""
        lat = np.linspace(point1["lat"], point2["lat"], n_points)
        lon = np.linspace(point1["lon"], point2["lon"], n_points)
        elev = np.linspace(point1.get("elevation", 0), point2.get("elevation", 0), n_points)
        
        return [
            {"lat": lat[i], "lon": lon[i], "elevation": elev[i]}
            for i in range(n_points)
        ]

    def _identify_structural_features(self, survey_data: Dict) -> List[Dict]:
        """Identify structural features like faults or folds"""
        # This would be more sophisticated in a real implementation
        features = []
        
        # Simple example: if elevation changes dramatically, might be a fault
        coordinates = survey_data.get("coordinates", [])
        if len(coordinates) > 1:
            elev_changes = [
                abs(coordinates[i+1].get("elevation", 0) - coordinates[i].get("elevation", 0))
                for i in range(len(coordinates)-1)
            ]
            
            if max(elev_changes) > 50:  # Threshold for fault (50 meters)
                max_idx = elev_changes.index(max(elev_changes))
                features.append({
                    "type": "fault",
                    "coordinates": [
                        coordinates[max_idx],
                        coordinates[max_idx+1]
                    ],
                    "displacement": elev_changes[max_idx]
                })
                
        return features