from PIL import Image

for img_name in ['spike_small.png', 'spike_large.png']:
    img = Image.open(img_name).convert('RGBA')
    w, h = img.size
    rightmost_alpha = [img.getpixel((w-1, y))[3] for y in range(h)]
    print(f'{img_name} rightmost column max alpha:', max(rightmost_alpha))
    print(f'{img_name} rightmost column avg alpha:', sum(rightmost_alpha)/len(rightmost_alpha))

    leftmost_alpha = [img.getpixel((0, y))[3] for y in range(h)]
    print(f'{img_name} leftmost column max alpha:', max(leftmost_alpha))
    print(f'{img_name} leftmost column avg alpha:', sum(leftmost_alpha)/len(leftmost_alpha))
