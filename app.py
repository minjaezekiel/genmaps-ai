import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disables oneDNN warnings
from core.geological_engine import GeologicalEngine
from core.survey_manager import SurveyManager
from utils.online_learner import OnlineLearner
from utils.map_generator import MapGenerator
from utils.survey_processor import SurveyProcessor
import argparse
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description="Geological Exploration AI System")
    parser.add_argument('--identify', type=str, help="Identify a rock or mineral from image")
    parser.add_argument('--search', type=str, help="Search for rock or mineral by property")
    parser.add_argument('--generate-map', type=str, help="Generate geological map from survey ID")
    parser.add_argument('--update', action='store_true', help="Update knowledge base from online sources")
    parser.add_argument('--new-survey', action='store_true', help="Start a new geological survey")
    parser.add_argument('--add-description', nargs=2, metavar=('SURVEY_ID', 'DESCRIPTION'), 
                       help="Add description to a survey")
    
    args = parser.parse_args()
    engine = GeologicalEngine()
    online_learner = OnlineLearner()
    map_generator = MapGenerator()
    survey_manager = SurveyManager()
    survey_processor = SurveyProcessor()
    
    if args.update:
        print("Updating knowledge base from online sources...")
        online_learner.update_knowledge_base()
        print("Knowledge base updated successfully.")
        
    elif args.identify:
        print(f"Identifying sample from {args.identify}...")
        try:
            result = engine.identify_mineral(args.identify) or engine.identify_rock(args.identify)
            if result:
                print("\nIdentification Result:")
                for key, value in result.items():
                    print(f"{key.capitalize()}: {value}")
            else:
                print("Could not identify the sample.")
        except Exception as e:
            print(f"Error during identification: {e}")
            
    elif args.search:
        print(f"Searching for {args.search}...")
        # Implement search functionality
        pass
        
    elif args.generate_map:
        print(f"Generating geological map for survey {args.generate_map}...")
        survey_data = survey_manager.get_survey_for_mapping(args.generate_map)
        if survey_data:
            processed_data = survey_processor.process_survey_data(survey_data)
            fig = map_generator.generate_detailed_map(processed_data)
            plt.show()
        else:
            print(f"Survey {args.generate_map} not found.")
            
    elif args.new_survey:
        print("Starting new geological survey...")
        print("Enter coordinates in format 'lat,lon,elevation' (one per line, empty line to finish):")
        coordinates = []
        while True:
            coord_input = input("> ")
            if not coord_input:
                break
            try:
                lat, lon, elev = map(float, coord_input.split(','))
                coordinates.append({"lat": lat, "lon": lon, "elevation": elev})
            except:
                print("Invalid format. Use 'lat,lon,elevation'")
        
        formation = input("Geological formation (optional): ")
        survey_id = survey_manager.create_survey(coordinates, formation)
        print(f"Created new survey with ID: {survey_id}")
        
    elif args.add_description:
        survey_id, description = args.add_description
        print(f"Adding description to survey {survey_id}...")
        result = survey_manager.add_description(survey_id, description)
        
        if result:
            print(f"\nInferred {result['type']}: {result['data']['name']}")
            print("Details:")
            for key, value in result['data'].items():
                if key != 'name':
                    print(f"{key.capitalize()}: {value}")
        else:
            print("Could not infer type from description.")
        
    else:
        print("No valid command provided. Use --help for usage information.")

if __name__ == "__main__":
    main()