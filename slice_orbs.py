from PIL import Image, ImageDraw
import os
import math

img_path = '/Users/aydenwang/.gemini/antigravity/brain/eca2ddf8-1d00-457e-aa92-8e24a354ebb8/media__1782161168153.png'
img = Image.open(img_path).convert("RGBA")

w, h = img.size
cell_w = w / 3.0
cell_h = h / 3.0

idx = 1
for row in range(3):
    for col in range(3):
        # Crop the cell
        left = int(col * cell_w)
        upper = int(row * cell_h)
        right = int((col + 1) * cell_w)
        lower = int((row + 1) * cell_h)
        
        cell = img.crop((left, upper, right, lower))
        
        # We need to find the actual bounding box of the orb within the cell
        # Let's make everything that is near-white transparent FIRST, but only on the edges?
        # Actually, if we just convert white to transparent, it might punch holes.
        # Let's do a flood fill from the corner (0,0) replacing near-white with transparent.
        
        # Convert to numpy for flood fill
        # Or simpler: The white background is contiguous from the corners.
        
        from PIL import ImageDraw
        # Create a mask image, floodfill from (0,0)
        # But PIL ImageDraw.floodfill acts on RGB, let's use a simpler approach.
        
        import numpy as np
        data = np.array(cell)
        
        # A simple circular mask based on the center of the orb.
        # Let's find the center of the non-white pixels.
        # white threshold
        r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
        is_white = (r > 240) & (g > 240) & (b > 240)
        
        # find bounding box of not white
        y_indices, x_indices = np.where(~is_white)
        if len(y_indices) == 0:
            continue
            
        min_x, max_x = np.min(x_indices), np.max(x_indices)
        min_y, max_y = np.min(y_indices), np.max(y_indices)
        
        # Center and radius
        cx = (min_x + max_x) / 2.0
        cy = (min_y + max_y) / 2.0
        radius = min((max_x - min_x)/2.0, (max_y - min_y)/2.0)
        
        # Make pixels outside the radius transparent
        Y, X = np.ogrid[:cell.size[1], :cell.size[0]]
        dist_from_center = np.sqrt((X - cx)**2 + (Y - cy)**2)
        
        # We want to keep the white inside the orb! So only make white transparent IF it is OUTSIDE a certain radius.
        # Actually, let's just make the white background transparent if it's far from the center.
        # What if we just use the white mask, but ONLY apply it to pixels > radius * 0.9?
        
        mask_to_clear = is_white & (dist_from_center > radius * 0.8)
        data[mask_to_clear, 3] = 0 # alpha = 0
        
        # Also enforce a hard circular crop slightly outside the orb to remove any artifacts
        data[dist_from_center > radius * 1.05, 3] = 0
        
        final_img = Image.fromarray(data)
        
        # Crop tightly to the orb
        bbox = final_img.getbbox()
        if bbox:
            final_img = final_img.crop(bbox)
            # resize a bit so they aren't huge (they might be 300x300, 100x100 is plenty for the game)
            final_img.thumbnail((120, 120), Image.LANCZOS)
            final_img.save(f'orb_{idx}.png')
            print(f"Saved orb_{idx}.png")
        idx += 1

print("Done slicing orbs.")
