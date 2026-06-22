from PIL import Image
import numpy as np

img_path = '/Users/aydenwang/.gemini/antigravity/brain/eca2ddf8-1d00-457e-aa92-8e24a354ebb8/media__1782163359363.png'
img = Image.open(img_path).convert("RGBA")

data = np.array(img)

# The image might have a solid white background (255, 255, 255).
# Let's check the top-left pixel. If it's white, we'll assume white background and remove it.
top_left = data[0,0]
if top_left[0] > 240 and top_left[1] > 240 and top_left[2] > 240 and top_left[3] > 240:
    print("Detected white background. Removing...")
    r, g, b, a = data.T
    white_areas = (r > 230) & (g > 230) & (b > 230)
    data[..., :-1][white_areas.T] = (0, 0, 0)
    data[..., -1][white_areas.T] = 0
    img2 = Image.fromarray(data)
    
    # Auto-crop alpha
    bbox = img2.getbbox()
    if bbox:
        img2 = img2.crop(bbox)
        
    img2.save("confirm_btn.png")
else:
    print("Background seems transparent/dark already. Just copying and cropping.")
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    img.save("confirm_btn.png")

print("Saved confirm_btn.png")
