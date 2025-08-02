```markdown
# Genmaps-AI Exploration System

![Geological Mapping Example](output/example_map.png)

A Python-based system for mineral exploration, rock identification, and geological mapping using machine learning and geospatial analysis.

## Features

- 🪨 Rock and mineral identification from images
- 🗺️ Geological map generation from survey data
- 📊 Knowledge base of geological formations
- 🔄 Continuous learning from online resources
- 📍 Coordinate-based survey system

## Installation

### Prerequisites

- Python 3.8+
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/minjaezekiel/genmaps-ai.git
cd geological-ai
```

2. Create and activate virtual environment:
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate    # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

```bash
python app.py [command] [arguments]
```

#### Available Commands:

| Command | Description | Example |
|---------|-------------|---------|
| `--identify` | Identify rock/mineral from image | `python app.py --identify samples/rock1.jpg` |
| `--new-survey` | Start new geological survey | `python app.py --new-survey` |
| `--add-description` | Add description to survey | `python app.py --add-description survey_001 "Granite with quartz veins"` |
| `--generate-map` | Generate map from survey | `python app.py --generate-map survey_001` |
| `--update` | Update knowledge base | `python app.py --update` |
| `--search` | Search knowledge base | `python app.py --search "hardness>5"` |

### Example Workflow

1. Start a new survey:
```bash
python app.py --new-survey
```

2. Add survey points (enter when done):
```
> 34.0522,-118.2437,71
> 34.0532,-118.2447,75
> 
```

3. Add descriptions:
```bash
python app.py --add-description survey_001 "Coarse-grained granite"
```

4. Generate map:
```bash
python app.py --generate-map survey_001
```

## Project Structure

```
geological_ai/
├── core/               # Core functionality
│   ├── geological_engine.py
│   ├── knowledge_base.py
│   └── survey_manager.py
├── utils/              # Utility modules
│   ├── map_generator.py
│   ├── online_learner.py
│   └── survey_processor.py
├── data/               # Data files
│   ├── minerals.json
│   ├── rocks.json
│   └── surveys/
├── models/             # ML models
├── output/             # Generated maps
├── tests/              # Unit tests
├── app.py              # Main application
└── requirements.txt    # Dependencies
```

## Code Documentation

### Core Modules

#### `geological_engine.py`
```python
class GeologicalEngine:
    """Main engine for geological analysis and identification"""
    
    def identify_mineral(self, image_path: str) -> Dict:
        """Identify mineral from image using ML model"""
        
    def generate_geological_map(self, survey_data: Dict) -> str:
        """Generate 2D map from survey coordinates"""
```

#### `map_generator.py`
```python
class MapGenerator:
    """Handles geological map visualization"""
    
    def generate_detailed_map(self, survey_data: Dict) -> str:
        """Create and save map from survey data"""
```

### Data Formats

#### Survey Data Format
```json
{
    "id": "survey_001",
    "coordinates": [
        {"lat": 34.0522, "lon": -118.2437, "elevation": 71}
    ],
    "descriptions": [
        {
            "location_index": 0,
            "text": "Granite outcrop",
            "inferred_type": "Granite"
        }
    ]
}
```

## Contributing

We welcome contributions! Here's how to help:

### How to Contribute

1. **Report Issues**:
   - Use GitHub Issues to report bugs or suggest features
   - Include error messages and reproduction steps

2. **Improve Documentation**:
   - Update README with new features
   - Add docstrings to Python code
   - Create tutorial notebooks

3. **Add Geological Data**:
   - Contribute to `data/minerals.json` and `data/rocks.json`
   - Include sources for any new data

4. **Enhance Models**:
   - Improve ML model accuracy
   - Add new classification categories
   - Contribute training data

5. **Enhance/add new features in code**:
    -Add new features into the app
    -Making the app user friendly
    -Fixing bugs/issues.

### Development Setup

1. Install development dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests:
```bash
pytest tests/
```

3. Before submitting PR:
- Format code with black:
```bash
black .
```
- Check for linting errors:
```bash
flake8
```

## License

MIT License - See [LICENSE](LICENSE) for details

## Acknowledgments

- USGS Geological Survey data
- Mindat.org mineral database
- TensorFlow/Keras for machine learning
```

This README includes:

1. **Project Overview** - Quick description and features
2. **Installation Guide** - Step-by-step setup instructions
3. **Usage Documentation** - CLI commands and examples
4. **Code Structure** - Directory layout explanation
5. **API Documentation** - Key modules and methods
6. **Contribution Guide** - How to help improve the project
7. **Development Practices** - Testing and code quality
8. **License Info** - Usage rights

>>>>>>> 1040537 (created functional version of geological-ai (genmap))
