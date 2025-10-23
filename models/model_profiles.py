"""
Multi-Model Processing Profiles
Different algorithms for different speed/quality needs
"""

from PIL import Image, ImageEnhance, ImageFilter
from enum import Enum

class ProcessingMode(Enum):
    """Processing mode options"""
    FAST = "fast"           # 0.3s - Quick preview
    BALANCED = "balanced"   # 1.0s - Good quality
    QUALITY = "quality"     # 2.0s - Professional
    ULTRA = "ultra"         # 3.0s - Maximum quality

def get_processing_params(mode: ProcessingMode, intensity: float):
    """
    Get processing parameters based on mode and intensity
    
    Returns: dict with processing configuration
    """
    if mode == ProcessingMode.FAST:
        return {
            'multi_scale': False,
            'edge_preserve': False,
            'histogram_enhance': False,
            'detail_recovery': False,
            'texture_enhance': False,
            'unsharp_strength': 1.0 + intensity * 0.3,
            'contrast_factor': 1.0 + intensity * 0.1,
            'color_factor': 1.0,
            'description': 'Fast Mode - Lightning speed preview'
        }
    
    elif mode == ProcessingMode.BALANCED:
        return {
            'multi_scale': intensity > 0.5,
            'edge_preserve': False,
            'histogram_enhance': True,
            'detail_recovery': intensity > 0.6,
            'texture_enhance': False,
            'unsharp_strength': 1.2 + intensity * 0.4,
            'contrast_factor': 1.0 + intensity * 0.15,
            'color_factor': 1.0 + intensity * 0.1,
            'description': 'Balanced Mode - Optimal speed/quality'
        }
    
    elif mode == ProcessingMode.QUALITY:
        return {
            'multi_scale': True,
            'edge_preserve': True,
            'histogram_enhance': True,
            'detail_recovery': True,
            'texture_enhance': intensity > 0.7,
            'unsharp_strength': 1.3 + intensity * 0.5,
            'contrast_factor': 1.0 + intensity * 0.2,
            'color_factor': 1.0 + intensity * 0.15,
            'description': 'Quality Mode - Professional results'
        }
    
    else:  # ULTRA
        return {
            'multi_scale': True,
            'edge_preserve': True,
            'histogram_enhance': True,
            'detail_recovery': True,
            'texture_enhance': True,
            'unsharp_strength': 1.5 + intensity * 0.7,
            'contrast_factor': 1.1 + intensity * 0.3,
            'color_factor': 1.1 + intensity * 0.2,
            'description': 'Ultra Mode - Maximum quality'
        }

def select_mode_from_intensity(intensity: float) -> ProcessingMode:
    """Auto-select processing mode based on intensity"""
    if intensity < 0.3:
        return ProcessingMode.FAST
    elif intensity < 0.6:
        return ProcessingMode.BALANCED
    elif intensity < 0.85:
        return ProcessingMode.QUALITY
    else:
        return ProcessingMode.ULTRA

