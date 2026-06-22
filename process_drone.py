from PIL import Image

def process():
    img_path = '/Users/aydenwang/.gemini/antigravity/brain/eca2ddf8-1d00-457e-aa92-8e24a354ebb8/media__1782083640593.jpg'
    img = Image.open(img_path).convert('RGBA')
    
    # Remove black background
    data = img.getdata()
    new_data = []
    for item in data:
        # If it's very dark (almost black), make it transparent
        if item[0] < 25 and item[1] < 25 and item[2] < 25:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    
    # Crop transparent edges
    w, h = img.size
    left, top, right, bottom = w, h, 0, 0
    for y in range(h):
        for x in range(w):
            if img.getpixel((x, y))[3] > 10:
                if x < left: left = x
                if y < top: top = y
                if x > right: right = x
                if y > bottom: bottom = y
                
    cropped = img.crop((left, top, right + 1, bottom + 1))
    
    # Scale it down to a reasonable size for the game (e.g., width ~120px)
    ratio = 120 / cropped.width
    new_size = (int(cropped.width * ratio), int(cropped.height * ratio))
    scaled = cropped.resize(new_size, Image.Resampling.LANCZOS)
    
    scaled.save('drone.png')
    print("Saved drone.png. Final size:", scaled.size)

process()
