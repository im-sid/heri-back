"""
FINAL Image Analysis - NO NUMPY REQUIRED
Pure PIL implementation with optimizations
Generates 5 analysis outputs
"""

from PIL import Image, ImageFilter, ImageChops, ImageEnhance
import io
import base64

# Pre-computed heat map colors (256 RGB triplets)
_HEAT_MAP_COLORS = None

def _init_heat_map():
    """Initialize heat map color palette"""
    global _HEAT_MAP_COLORS
    if _HEAT_MAP_COLORS:
        return
    
    _HEAT_MAP_COLORS = []
    for i in range(256):
        if i < 51:  # Blue
            _HEAT_MAP_COLORS.append((0, 0, int(i * 5.1)))
        elif i < 102:  # Cyan
            _HEAT_MAP_COLORS.append((0, int((i - 51) * 5.1), 255))
        elif i < 153:  # Green
            _HEAT_MAP_COLORS.append((0, 255, int(255 - (i - 102) * 5.1)))
        elif i < 204:  # Yellow
            _HEAT_MAP_COLORS.append((int((i - 153) * 5.1), 255, 0))
        else:  # Red
            _HEAT_MAP_COLORS.append((255, int(255 - (i - 204) * 5.1), 0))

def generate_edge_detection(image):
    """Edge detection output"""
    gray = image.convert('L')
    edges = gray.filter(ImageFilter.FIND_EDGES)
    # Threshold using point() - optimized
    edges = edges.point(lambda x: 255 if x > 50 else 0)
    return edges.convert('RGB')

def generate_heat_map(image):
    """Heat map with pre-computed colors"""
    _init_heat_map()
    gray = image.convert('L')
    heat_map = Image.new('RGB', gray.size)
    
    # Use putdata with pre-computed colors (fast)
    pixels = list(gray.getdata())
    heat_pixels = [_HEAT_MAP_COLORS[p] for p in pixels]
    heat_map.putdata(heat_pixels)
    
    return heat_map

def generate_detail_enhancement(image):
    """Detail enhancement output"""
    detailed = image.filter(ImageFilter.DETAIL)
    detailed = detailed.filter(ImageFilter.SHARPEN)
    detailed = detailed.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return detailed

def generate_grayscale_analysis(image):
    """Grayscale analysis output"""
    gray = image.convert('L')
    enhancer = ImageEnhance.Contrast(gray)
    enhanced = enhancer.enhance(1.5)
    return enhanced.convert('RGB')

def generate_texture_map(image):
    """Texture map output"""
    gray = image.convert('L')
    blurred = gray.filter(ImageFilter.GaussianBlur(radius=3))
    texture = ImageChops.difference(gray, blurred)
    enhancer = ImageEnhance.Contrast(texture)
    texture = enhancer.enhance(3.0)
    return texture.convert('RGB')

def _encode_image(img):
    """Encode PIL Image to base64"""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG", optimize=True)
    return base64.b64encode(buffered.getvalue()).decode()

def generate_all_analysis_outputs(image):
    """
    Generate all 5 analysis outputs
    Sequential but optimized with pre-computed colors
    """
    print("\n[ANALYSIS] 🚀 Generating 5 outputs...")
    
    outputs = {}
    
    try:
        print("[ANALYSIS] 1/5: Edge detection...")
        outputs['edges'] = _encode_image(generate_edge_detection(image))
        
        print("[ANALYSIS] 2/5: Heat map...")
        outputs['heat_map'] = _encode_image(generate_heat_map(image))
        
        print("[ANALYSIS] 3/5: Detail enhancement...")
        outputs['details'] = _encode_image(generate_detail_enhancement(image))
        
        print("[ANALYSIS] 4/5: Grayscale analysis...")
        outputs['grayscale'] = _encode_image(generate_grayscale_analysis(image))
        
        print("[ANALYSIS] 5/5: Texture map...")
        outputs['texture'] = _encode_image(generate_texture_map(image))
        
        print(f"[ANALYSIS] ✅ All {len(outputs)} outputs ready!\n")
        
    except Exception as e:
        print(f"[ANALYSIS] ❌ Error: {e}")
    
    return outputs

