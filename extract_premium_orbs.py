import numpy as np
from PIL import Image

def make_transparent(img, black_thresh=30):
    img = img.convert("RGBA")
    data = np.array(img)
    # The image is on a pure black background.
    # Calculate luminance or just max RGB.
    rgb = data[:,:,:3]
    max_val = np.max(rgb, axis=2)
    
    # Simple thresholding: make black fully transparent, leave bright parts opaque.
    # To avoid hard edges, we can map brightness to alpha for very dark pixels.
    alpha = np.where(max_val < black_thresh, 0, 255)
    
    # Smooth alpha blending for anti-aliasing
    # For values between black_thresh and black_thresh+30, fade in
    fade_mask = (max_val >= black_thresh) & (max_val < black_thresh + 40)
    alpha[fade_mask] = ((max_val[fade_mask] - black_thresh) / 40 * 255).astype(np.uint8)

    data[:,:,3] = alpha
    return Image.fromarray(data)

img_path = "/Users/aydenwang/.gemini/antigravity/brain/eca2ddf8-1d00-457e-aa92-8e24a354ebb8/media__1782168700018.jpg"
img = Image.open(img_path)
w, h = img.size
cell_w = w // 3
cell_h = h // 3

orb_idx = 10
for row in range(3):
    for col in range(3):
        box = (col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h)
        cell = img.crop(box)
        
        # Center crop slightly if needed to remove edges, but 341x341 is tight enough
        # We can crop 10px from edges to be safe
        cell = cell.crop((10, 10, cell_w-10, cell_h-10))
        
        # Make transparent
        transparent_cell = make_transparent(cell, black_thresh=20)
        
        transparent_cell.save(f"premium_orb_{orb_idx}.png")
        print(f"Saved premium_orb_{orb_idx}.png")
        orb_idx += 1
