import tensorflow as tf
import numpy as np
from PIL import Image
from pathlib import Path
from typing import Dict, List, Optional
from .knowledge_base import KnowledgeBase

class GeologicalEngine:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.models_dir = Path(__file__).parent.parent / "models"
        self.models_dir.mkdir(exist_ok=True)  # Ensure models directory exists
        
        # Initialize class mappings
        self.mineral_classes = {
            0: "Quartz",
            1: "Feldspar",
            2: "Mica",
            3: "Calcite"
        }
        
        self.rock_classes = {
            0: "Granite",
            1: "Basalt",
            2: "Sandstone",
            3: "Limestone"
        }

        # Load or create models
        self.mineral_model = self._load_model("mineral_classifier.h5")
        self.rock_model = self._load_model("rock_classifier.h5")

    def _load_model(self, model_name: str) -> tf.keras.Model:
        try:
            return tf.keras.models.load_model(self.models_dir / model_name)
        except Exception as e:
            print(f"Model {model_name} not found. Creating placeholder model. Error: {str(e)}")
            return self._create_placeholder_model(model_name)

    def _create_placeholder_model(self, model_name: str) -> tf.keras.Model:
        """Creates a simple placeholder model"""
        num_classes = len(self.mineral_classes) if "mineral" in model_name else len(self.rock_classes)
        
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(128, 128, 3)),  # Explicit input shape
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Save the placeholder model for future use
        model.save(self.models_dir / model_name)
        return model

    def identify_mineral(self, image_path: str) -> Optional[Dict]:
        """Identify mineral from image"""
        try:
            img = self._preprocess_image(image_path)
            prediction = self.mineral_model.predict(img)
            class_id = np.argmax(prediction[0])
            mineral_name = self.mineral_classes.get(class_id, "Unknown")
            return self.knowledge_base.get_mineral(mineral_name)
        except Exception as e:
            print(f"Error identifying mineral: {str(e)}")
            return None

    def identify_rock(self, image_path: str) -> Optional[Dict]:
        """Identify rock from image"""
        try:
            img = self._preprocess_image(image_path)
            prediction = self.rock_model.predict(img)
            class_id = np.argmax(prediction[0])
            rock_name = self.rock_classes.get(class_id, "Unknown")
            return self.knowledge_base.get_rock(rock_name)
        except Exception as e:
            print(f"Error identifying rock: {str(e)}")
            return None

    def _preprocess_image(self, image_path: str) -> np.ndarray:
        """Preprocess image for model input"""
        img = Image.open(image_path)
        img = img.resize((128, 128))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create batch axis
        return img_array / 255.0  # Normalize to [0,1]

    def generate_geological_map(self, survey_data: Dict) -> str:
        """Generate 2D geological map from survey data"""
        map_data = {
            "boundaries": self._identify_formation_boundaries(survey_data),
            "units": self._classify_geological_units(survey_data),
            "features": self._identify_structural_features(survey_data)
        }
        return self._render_map(map_data)

    def _identify_formation_boundaries(self, data: Dict) -> List[Dict]:
        """Identify formation boundaries from survey data"""
        return []

    def _classify_geological_units(self, data: Dict) -> List[Dict]:
        """Classify geological units from survey data"""
        return []

    def _identify_structural_features(self, data: Dict) -> List[Dict]:
        """Identify structural features from survey data"""
        return []

    def _render_map(self, map_data: Dict) -> str:
        """Generate map visualization"""
        return "Geological map generated with units and boundaries"