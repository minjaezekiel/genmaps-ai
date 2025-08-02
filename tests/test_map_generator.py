import unittest
from utils.map_generator import MapGenerator

class TestMapGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = MapGenerator()
        self.test_data = {
            "coordinates": [{"lat": 34.0, "lon": -118.0, "elevation": 100}],
            "units": [{
                "type": "granite",
                "coordinates": [{"lat": 34.0, "lon": -118.0, "elevation": 100}],
                "description": "Test granite"
            }]
        }

    def test_map_creation(self):
        fig = self.generator.generate_detailed_map(self.test_data)
        self.assertIsNotNone(fig)

if __name__ == '__main__':
    unittest.main()