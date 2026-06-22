import re

with open('game.html', 'r') as f:
    html = f.read()

# Replace the nulls with the new titleSrc names
html = html.replace("{ id: 0, name: 'Default Neon', color: '#00ffff', src: 'none', titleSrc: null }", "{ id: 0, name: 'Default Neon', color: '#00ffff', src: 'none', titleSrc: 'title_0.png' }")
html = html.replace("{ id: 2, name: 'Crimson Eye', color: '#ff2222', src: 'orb_2.png', titleSrc: null }", "{ id: 2, name: 'Crimson Eye', color: '#ff2222', src: 'orb_2.png', titleSrc: 'title_2.png' }")
html = html.replace("{ id: 4, name: 'Amethyst Void', color: '#8822ff', src: 'orb_4.png', titleSrc: null }", "{ id: 4, name: 'Amethyst Void', color: '#8822ff', src: 'orb_4.png', titleSrc: 'title_4.png' }")
html = html.replace("{ id: 6, name: 'Molten Core', color: '#ff8822', src: 'orb_6.png', titleSrc: null }", "{ id: 6, name: 'Molten Core', color: '#ff8822', src: 'orb_6.png', titleSrc: 'title_6.png' }")
html = html.replace("{ id: 8, name: 'Magenta Spark', color: '#ff22ff', src: 'orb_8.png', titleSrc: null }", "{ id: 8, name: 'Magenta Spark', color: '#ff22ff', src: 'orb_8.png', titleSrc: 'title_8.png' }")

with open('game.html', 'w') as f:
    f.write(html)
print("Updated game.html with new titles!")
