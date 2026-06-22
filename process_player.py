from PIL import Image
import numpy as np

# Load the raw image
img_path = '/Users/aydenwang/.gemini/antigravity/brain/eca2ddf8-1d00-457e-aa92-8e24a354ebb8/media__1782160652944.png'
img = Image.open(img_path).convert('RGBA')

# Convert to numpy array
data = np.array(img)

# The image has a black background. We want to convert black to transparent.
# Let's find pixels where R, G, B are all very low (e.g., < 20)
r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
black_areas = (r < 25) & (g < 25) & (b < 25)
data[black_areas, 3] = 0

# Create new image with transparency
transparent_img = Image.fromarray(data)

# Now, crop tightly to the non-transparent area
bbox = transparent_img.getbbox()
if bbox:
    transparent_img = transparent_img.crop(bbox)

# Save to the project directory
transparent_img.save('player.png')
print("Processed player image and saved to player.png")
