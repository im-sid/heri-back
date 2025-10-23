"""
EXTREME FAST Analysis
Maximum speed - smaller images, JPEG compression
"""

from PIL import Image, ImageFilter, ImageChops, ImageEnhance, ImageOps
import io
import base64
import time

def generate_all_analysis_outputs(image):
    """
    EXTREME FAST - 5 outputs with aggressive optimization
    """
    start = time.time()
    outputs = {}
    
    try:
        # VERY SMALL for speed
        max_size = 400
        if image.width > max_size or image.height > max_size:
            ratio = min(max_size / image.width, max_size / image.height)
            new_size = (int(image.width * ratio), int(image.height * ratio))
            image = image.resize(new_size, Image.Resampling.BILINEAR)
        
        gray = image.convert('L')
        
        # 1. EDGES (fastest filter)
        edges = gray.filter(ImageFilter.FIND_EDGES)
        buffered = io.BytesIO()
        edges.convert('RGB').save(buffered, format="JPEG", quality=80, optimize=False)
        outputs['edge_detection'] = 'data:image/jpeg;base64,' + base64.b64encode(buffered.getvalue()).decode()
        
        # 2. HEAT MAP (fast colorize)
        heat = ImageOps.colorize(gray, black="blue", white="red")
        buffered = io.BytesIO()
        heat.save(buffered, format="JPEG", quality=80, optimize=False)
        outputs['heat_map'] = 'data:image/jpeg;base64,' + base64.b64encode(buffered.getvalue()).decode()
        
        # 3. DETAILS (fast filter)
        detailed = image.filter(ImageFilter.DETAIL)
        buffered = io.BytesIO()
        detailed.save(buffered, format="JPEG", quality=80, optimize=False)
        outputs['detail_enhancement'] = 'data:image/jpeg;base64,' + base64.b64encode(buffered.getvalue()).decode()
        
        # 4. LUMINANCE (just enhanced grayscale)
        enhanced = ImageEnhance.Contrast(gray).enhance(1.2)
        buffered = io.BytesIO()
        enhanced.convert('RGB').save(buffered, format="JPEG", quality=80, optimize=False)
        outputs['luminance_analysis'] = 'data:image/jpeg;base64,' + base64.b64encode(buffered.getvalue()).decode()
        
        # 5. TEXTURE (simple blur difference)
        blurred = gray.filter(ImageFilter.BLUR)
        texture = ImageChops.difference(gray, blurred)
        texture = ImageEnhance.Contrast(texture).enhance(1.8)
        buffered = io.BytesIO()
        texture.convert('RGB').save(buffered, format="JPEG", quality=80, optimize=False)
        outputs['texture_map'] = 'data:image/jpeg;base64,' + base64.b64encode(buffered.getvalue()).decode()
        
        total = time.time() - start
        print(f"[ANALYSIS] ALL 5 DONE in {total:.2f}s")
        
    except Exception as e:
        print(f"[ANALYSIS] ERROR: {e}")
    
    return outputs
