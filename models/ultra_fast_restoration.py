"""
PROFESSIONAL Restoration
High-quality adaptive pipeline
"""

from PIL import Image, ImageEnhance, ImageFilter, ImageStat
import time

def restore_artifact_image(image, intensity=0.75, mode='auto'):
    """
    PROFESSIONAL Restoration with intelligent adaptive processing
    """
    start = time.time()
    print("\n" + "="*60)
    print("[RESTORATION] Professional Pipeline Starting...")
    print("="*60)
    
    # Step 1: Pre-processing and analysis
    print("[Stage 1/8] Image Analysis...")
    stage_start = time.time()
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize if too large
    max_size = 2000
    if image.width > max_size or image.height > max_size:
        ratio = min(max_size / image.width, max_size / image.height)
        new_size = (int(image.width * ratio), int(image.height * ratio))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    
    # Analyze image characteristics
    gray = image.convert('L')
    stat = ImageStat.Stat(gray)
    brightness = stat.mean[0]
    variance = stat.var[0]
    
    is_dark = brightness < 110
    is_bright = brightness > 170
    is_noisy = variance > 2500
    is_low_contrast = variance < 800
    
    print(f"[Stage 1/8] Complete in {time.time()-stage_start:.2f}s")
    print(f"  Analysis: Brightness={brightness:.1f}, Variance={variance:.1f}")
    print(f"  Flags: Dark={is_dark}, Bright={is_bright}, Noisy={is_noisy}, LowContrast={is_low_contrast}")
    
    result = image
    
    # Step 2: Adaptive denoising
    print("[Stage 2/8] Adaptive Denoising...")
    stage_start = time.time()
    if is_noisy:
        result = result.filter(ImageFilter.MedianFilter(size=3))
        result = result.filter(ImageFilter.SMOOTH_MORE)
        print(f"[Stage 2/8] Complete in {time.time()-stage_start:.2f}s | Denoised (noisy image detected)")
    else:
        print(f"[Stage 2/8] Skipped (clean image)")
    
    # Step 3: Edge-preserving sharpening
    print("[Stage 3/8] Edge-Preserving Sharpening...")
    stage_start = time.time()
    sharpness = 1.7 + (intensity * 1.0)
    result = ImageEnhance.Sharpness(result).enhance(sharpness)
    print(f"[Stage 3/8] Complete in {time.time()-stage_start:.2f}s | Sharpness: {sharpness:.2f}x")
    
    # Step 4: Adaptive contrast restoration
    print("[Stage 4/8] Adaptive Contrast Restoration...")
    stage_start = time.time()
    if is_low_contrast:
        contrast = 1.4 + (intensity * 0.5)
    elif is_dark:
        contrast = 1.35 + (intensity * 0.45)
    elif is_bright:
        contrast = 1.25 + (intensity * 0.35)
    else:
        contrast = 1.2 + (intensity * 0.3)
    
    result = ImageEnhance.Contrast(result).enhance(contrast)
    print(f"[Stage 4/8] Complete in {time.time()-stage_start:.2f}s | Contrast: {contrast:.2f}x (Adaptive)")
    
    # Step 5: Color restoration
    print("[Stage 5/8] Color Restoration...")
    stage_start = time.time()
    color = 1.2 + (intensity * 0.3)
    result = ImageEnhance.Color(result).enhance(color)
    print(f"[Stage 5/8] Complete in {time.time()-stage_start:.2f}s | Color: {color:.2f}x")
    
    # Step 6: Detail enhancement with unsharp mask
    print("[Stage 6/8] Detail Enhancement...")
    stage_start = time.time()
    if intensity > 0.5:
        radius = 1.5 + (intensity * 1.0)
        percent = int(120 + intensity * 80)
        result = result.filter(ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=2))
        print(f"[Stage 6/8] Complete in {time.time()-stage_start:.2f}s | Unsharp: radius={radius:.1f}, percent={percent}")
    else:
        print(f"[Stage 6/8] Skipped (low intensity)")
    
    # Step 7: Adaptive brightness correction
    print("[Stage 7/8] Adaptive Brightness Correction...")
    stage_start = time.time()
    if is_dark:
        brightness_factor = 1.15 + (intensity * 0.15)
        result = ImageEnhance.Brightness(result).enhance(brightness_factor)
        print(f"[Stage 7/8] Complete in {time.time()-stage_start:.2f}s | Brightened: {brightness_factor:.2f}x")
    elif is_bright:
        brightness_factor = 0.90 + (intensity * 0.05)
        result = ImageEnhance.Brightness(result).enhance(brightness_factor)
        print(f"[Stage 7/8] Complete in {time.time()-stage_start:.2f}s | Dimmed: {brightness_factor:.2f}x")
    else:
        print(f"[Stage 7/8] Skipped (optimal brightness)")
    
    # Step 8: Final polish
    print("[Stage 8/8] Final Polish...")
    stage_start = time.time()
    if intensity > 0.8:
        result = result.filter(ImageFilter.EDGE_ENHANCE)
        print(f"[Stage 8/8] Complete in {time.time()-stage_start:.2f}s | Edge enhancement applied")
    else:
        print(f"[Stage 8/8] Skipped")
    
    total = time.time() - start
    print("="*60)
    print(f"[RESTORATION] COMPLETE in {total:.2f}s")
    print(f"Adaptive Processing: {sum([is_dark, is_bright, is_noisy, is_low_contrast])} conditions addressed")
    print("="*60 + "\n")
    
    return result, {
        'processing_time': f'{total:.2f}s',
        'algorithm': 'Professional 8-Stage Adaptive Restoration',
        'quality': 'High',
        'adaptive_flags': {
            'dark': is_dark,
            'bright': is_bright,
            'noisy': is_noisy,
            'low_contrast': is_low_contrast
        },
        'status': 'SUCCESS'
    }
