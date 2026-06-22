from PIL import Image

def trim_transparent_edges(img_path):
    img = Image.open(img_path).convert('RGBA')
    w, h = img.size
    
    # Find bounding box of pixels with alpha > 100
    left = w
    top = h
    right = 0
    bottom = 0
    
    for y in range(h):
        for x in range(w):
            alpha = img.getpixel((x, y))[3]
            if alpha > 100:
                if x < left: left = x
                if y < top: top = y
                if x > right: right = x
                if y > bottom: bottom = y
                
    if left > right or top > bottom:
        print(f"{img_path} is completely transparent!")
        return
        
    print(f"Cropping {img_path} to {left}, {top}, {right}, {bottom}")
    cropped = img.crop((left, top, right + 1, bottom + 1))
    cropped.save(img_path)

for name in ['spike_small.png', 'spike_large.png']:
    trim_transparent_edges(name)
