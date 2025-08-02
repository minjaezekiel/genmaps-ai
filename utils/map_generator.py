import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging
from matplotlib.backends.backend_agg import FigureCanvasAgg

class MapGenerator:
    def __init__(self):
        """Initialize with color mappings and setup output directory"""
        self.color_map = {
            "granite": "#FF9999",
            "basalt": "#9999FF",
            "sandstone": "#FFCC99",
            "limestone": "#99FF99",
            "shale": "#CCCCCC",
            "quartz": "#FFFFFF",
            "feldspar": "#FFFF99",
            "unknown": "#777777"
        }
        self.output_dir = Path(__file__).parent.parent / "output"
        self.output_dir.mkdir(exist_ok=True)
        logging.basicConfig(level=logging.INFO)

    def generate_detailed_map(self, survey_data: Dict) -> Optional[str]:
        """
        Generate and save a detailed geological map from survey data
        
        Args:
            survey_data: Dictionary containing:
                - coordinates: List of {lat, lon, elevation}
                - units: Geological units data
                - boundaries: Boundary data
                - features: Structural features
                - id: Survey ID (optional)
                
        Returns:
            Path to saved map image or None if failed
        """
        try:
            fig = self._create_figure()
            ax = fig.add_subplot(111)
            
            # Plot all map elements
            self._plot_geological_features(ax, survey_data)
            
            # Add decorations
            self._add_map_decorations(ax, survey_data.get('id', ''))
            
            # Save and return path
            return self._save_map(fig, survey_data.get('id', 'survey'))
        except Exception as e:
            logging.error(f"Map generation failed: {str(e)}", exc_info=True)
            return None
        finally:
            plt.close('all')  # Ensure clean up

    def _create_figure(self) -> plt.Figure:
        """Create a properly configured figure"""
        fig = plt.figure(figsize=(12, 10), dpi=150)
        FigureCanvasAgg(fig)  # Set up proper canvas
        return fig

    def _plot_geological_features(self, ax: plt.Axes, data: Dict) -> None:
        """Plot all geological features on the map"""
        # Get coordinate bounds
        lats = [p['lat'] for p in data['coordinates']]
        lons = [p['lon'] for p in data['coordinates']]
        
        # Set plot limits with margin
        margin = 0.1
        ax.set_xlim(min(lons)-margin, max(lons)+margin)
        ax.set_ylim(min(lats)-margin, max(lats)+margin)
        
        # Plot coordinates
        ax.scatter(
            [p['lon'] for p in data['coordinates']],
            [p['lat'] for p in data['coordinates']],
            color='red', s=50, zorder=5, label='Survey Points'
        )
        
        # Plot units as polygons
        for unit in data.get('units', []):
            self._plot_unit(ax, unit)
            
        # Plot boundaries
        for boundary in data.get('boundaries', []):
            self._plot_boundary(ax, boundary)
            
        # Plot structural features
        for feature in data.get('structural_features', []):
            self._plot_structural_feature(ax, feature)

    def _plot_unit(self, ax: plt.Axes, unit: Dict) -> None:
        """Plot a geological unit polygon"""
        color = self.color_map.get(unit['type'].lower(), '#777777')
        lons = [p['lon'] for p in unit['coordinates']]
        lats = [p['lat'] for p in unit['coordinates']]
        
        poly = plt.Polygon(
            list(zip(lons, lats)),
            facecolor=color,
            alpha=0.6,
            edgecolor='k',
            linewidth=0.8,
            label=unit['type']
        )
        ax.add_patch(poly)
        
        # Add label if area is large enough
        if len(lons) > 2:
            centroid_lon, centroid_lat = np.mean(lons), np.mean(lats)
            ax.text(
                centroid_lon, centroid_lat,
                unit['type'],
                ha='center',
                va='center',
                fontsize=8,
                bbox=dict(facecolor='white', alpha=0.7, pad=2)
            )

    def _plot_boundary(self, ax: plt.Axes, boundary: Dict) -> None:
        """Plot boundary between geological units"""
        lons = [p['lon'] for p in boundary['coordinates']]
        lats = [p['lat'] for p in boundary['coordinates']]
        ax.plot(lons, lats, 'k--', linewidth=1.2, alpha=0.7)

    def _plot_structural_feature(self, ax: plt.Axes, feature: Dict) -> None:
        """Plot structural features like faults"""
        if feature['type'] == 'fault':
            lons = [p['lon'] for p in feature['coordinates']]
            lats = [p['lat'] for p in feature['coordinates']]
            line = ax.plot(lons, lats, 'r-', linewidth=2)[0]
            
            # Add fault label
            if len(lons) > 1:
                mid = len(lons) // 2
                ax.text(
                    lons[mid], lats[mid],
                    f"Fault ({feature.get('displacement', '?')}m)",
                    fontsize=8,
                    color='red',
                    rotation=self._calculate_angle(lons, lats, mid),
                    bbox=dict(facecolor='white', alpha=0.7)
                )

    def _calculate_angle(self, x: List[float], y: List[float], idx: int) -> float:
        """Calculate label rotation angle for features"""
        if idx == 0:
            dx = x[1] - x[0]
            dy = y[1] - y[0]
        else:
            dx = x[idx] - x[idx-1]
            dy = y[idx] - y[idx-1]
        return np.degrees(np.arctan2(dy, dx))

    def _add_map_decorations(self, ax: plt.Axes, survey_id: str) -> None:
        """Add title, legend, and other decorations"""
        ax.set_title(f"Geological Survey Map - {survey_id}", pad=20)
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.grid(True, linestyle=':', alpha=0.5)
        self._add_legend(ax)

    def _add_legend(self, ax: plt.Axes) -> None:
        """Add comprehensive legend to the map"""
        patches = [
            plt.Rectangle((0, 0), 1, 1, fc=color, alpha=0.6)
            for color in self.color_map.values()
        ]
        ax.legend(
            patches,
            self.color_map.keys(),
            title='Geological Units',
            loc='upper left',
            bbox_to_anchor=(1.05, 1),
            borderaxespad=0.
        )

    def _save_map(self, fig: plt.Figure, survey_id: str) -> str:
        """Save the generated map to file"""
        map_path = self.output_dir / f"geological_map_{survey_id}.png"
        fig.savefig(
            map_path,
            bbox_inches='tight',
            dpi=150,
            format='png'
        )
        logging.info(f"Map successfully saved to {map_path}")
        return str(map_path)