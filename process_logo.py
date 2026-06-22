from PIL import Image

def process():
    img_path = '/Users/aydenwang/.gemini/antigravity/brain/eca2ddf8-1d00-457e-aa92-8e24a354ebb8/media__1782085276104.jpg'
    img = Image.open(img_path).convert('RGBA')
    
    # Remove black background (mostly solid black on edges, but glows exist)
    # To handle glows nicely without clipping them harshly, we can map brightness to alpha
    # Since it's a neon logo on black, the luminosity *is* basically the alpha channel
    data = img.getdata()
    new_data = []
    for item in data:
        r, g, b, a = item
        # Calculate perceived brightness
        lum = int(0.299*r + 0.587*g + 0.114*b)
        
        # If it's pure black or very dark, make it transparent
        if r < 15 and g < 15 and b < 15:
            new_data.append((0, 0, 0, 0))
        else:
            # We want to keep the original color, but maybe feather the alpha based on max color channel
            # to preserve the glow effect naturally on dark backgrounds
            max_c = max(r, g, b)
            # If it's somewhat bright, keep it fully opaque to avoid looking washed out
            if max_c > 50:
                new_data.append(item)
            else:
                # Feathering very dark edges
                new_alpha = int((max_c / 50.0) * 255)
                new_data.append((r, g, b, new_alpha))
                
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
                
    # Add a small padding to the crop
    pad = 10
    left = max(0, left - pad)
    top = max(0, top - pad)
    right = min(w - 1, right + pad)
    bottom = min(h - 1, bottom + pad)
    
    cropped = img.crop((left, top, right + 1, bottom + 1))
    
    cropped.save('logo.png')
    print("Saved logo.png. Final size:", cropped.size)

process()
