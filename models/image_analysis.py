"""
Image Analysis & Visualization Generator
Produces 5 different analysis outputs for comparison
"""

from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageChops
import io
import base64

def generate_edge_detection(image):
    """Generate edge detection visualization"""
    try:
        # Convert to grayscale first
        gray = image.convert('L')
        # Apply edge detection
        edges = gray.filter(ImageFilter.FIND_EDGES)
        # Enhance for visibility
        edges = edges.point(lambda x: 255 if x > 50 else 0)
        # Convert back to RGB for display
        return edges.convert('RGB')
    except:
        return image.copy()

def generate_heat_map(image):
    """Generate heat map based on intensity"""
    try:
        # Convert to grayscale
        gray = image.convert('L')
        
        # Create heat map
        width, height = gray.size
        heat_map = Image.new('RGB', (width, height))
        pixels = heat_map.load()
        gray_pixels = gray.load()
        
        for y in range(height):
            for x in range(width):
                intensity = gray_pixels[x, y]
                # Map to color gradient: blue -> cyan -> green -> yellow -> red
                if intensity < 51:  # 0-50: Blue
                    r, g, b = 0, 0, int(intensity * 5.1)
                elif intensity < 102:  # 51-101: Cyan
                    r, g, b = 0, int((intensity - 51) * 5.1), 255
                elif intensity < 153:  # 102-152: Green
                    r, g, b = 0, 255, int(255 - (intensity - 102) * 5.1)
                elif intensity < 204:  # 153-203: Yellow
                    r, g, b = int((intensity - 153) * 5.1), 255, 0
                else:  # 204-255: Red
                    r, g, b = 255, int(255 - (intensity - 204) * 5.1), 0
                
                pixels[x, y] = (r, g, b)
        
        return heat_map
    except:
        return image.copy()

def generate_detail_enhancement(image):
    """Generate detail-enhanced version"""
    try:
        # Apply DETAIL filter
        detailed = image.filter(ImageFilter.DETAIL)
        # Apply SHARPEN
        detailed = detailed.filter(ImageFilter.SHARPEN)
        # Enhance edges
        detailed = detailed.filter(ImageFilter.EDGE_ENHANCE_MORE)
        return detailed
    except:
        return image.copy()

def generate_grayscale_analysis(image):
    """Generate grayscale luminance analysis"""
    try:
        # Convert to grayscale
        gray = image.convert('L')
        # Enhance contrast
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(gray)
        enhanced = enhancer.enhance(1.5)
        # Convert back to RGB
        return enhanced.convert('RGB')
    except:
        return image.copy()

def generate_texture_map(image):
    """Generate texture map showing surface details"""
    try:
        # Apply multiple filters to extract texture
        gray = image.convert('L')
        # High-pass filter simulation
        blurred = gray.filter(ImageFilter.GaussianBlur(radius=3))
        texture = ImageChops.difference(gray, blurred)
        # Enhance
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(texture)
        texture = enhancer.enhance(3.0)
        # Colorize for better visualization
        texture_rgb = texture.convert('RGB')
        return texture_rgb
    except:
        return image.copy()

def generate_all_analysis_outputs(image):
    """
    Generate all 5 analysis outputs
    Returns dict with base64 encoded images
    """
    print("\n[ANALYSIS] Generating 5 analysis outputs...")
    
    outputs = {}
    
    try:
        # 1. Edge Detection
        print("[ANALYSIS] 1/5: Edge detection...")
        edges = generate_edge_detection(image)
        buffered = io.BytesIO()
        edges.save(buffered, format="PNG")
        outputs['edges'] = base64.b64encode(buffered.getvalue()).decode()
        
        # 2. Heat Map
        print("[ANALYSIS] 2/5: Heat map...")
        heat_map = generate_heat_map(image)
        buffered = io.BytesIO()
        heat_map.save(buffered, format="PNG")
        outputs['heat_map'] = base64.b64encode(buffered.getvalue()).decode()
        
        # 3. Detail Enhancement
        print("[ANALYSIS] 3/5: Detail enhancement...")
        details = generate_detail_enhancement(image)
        buffered = io.BytesIO()
        details.save(buffered, format="PNG")
        outputs['details'] = base64.b64encode(buffered.getvalue()).decode()
        
        # 4. Grayscale Analysis
        print("[ANALYSIS] 4/5: Grayscale analysis...")
        grayscale = generate_grayscale_analysis(image)
        buffered = io.BytesIO()
        grayscale.save(buffered, format="PNG")
        outputs['grayscale'] = base64.b64encode(buffered.getvalue()).decode()
        
        # 5. Texture Map
        print("[ANALYSIS] 5/5: Texture map...")
        texture = generate_texture_map(image)
        buffered = io.BytesIO()
        texture.save(buffered, format="PNG")
        outputs['texture'] = base64.b64encode(buffered.getvalue()).decode()
        
        print("[ANALYSIS] ✅ All outputs generated!\n")
        
    except Exception as e:
        print(f"[ANALYSIS] Error: {e}")
        import traceback
        traceback.print_exc()
    
    return outputs

