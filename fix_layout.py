import re

# Fix game.html
with open('game.html', 'r') as f:
    game_html = f.read()

# Remove inline display: flex from left-ad and right-ad
game_html = re.sub(r'class="ad-space-desktop left-ad" style="[^"]*"', r'class="ad-space-desktop left-ad"', game_html)
game_html = re.sub(r'class="ad-space-desktop right-ad" style="[^"]*"', r'class="ad-space-desktop right-ad"', game_html)

# Center the desktop-main-layout
game_html = game_html.replace('class="desktop-main-layout" style="display: flex; flex: 1; width: 100%; height: 100%; overflow: hidden;"', 'class="desktop-main-layout" style="display: flex; flex: 1; width: 100%; height: 100%; overflow: hidden; justify-content: center;"')

with open('game.html', 'w') as f:
    f.write(game_html)

# Fix index.html
with open('index.html', 'r') as f:
    index_html = f.read()

index_html = re.sub(r'class="ad-space-desktop left-ad" style="[^"]*"', r'class="ad-space-desktop left-ad"', index_html)
index_html = re.sub(r'class="ad-space-desktop right-ad" style="[^"]*"', r'class="ad-space-desktop right-ad"', index_html)

index_html = index_html.replace('class="desktop-main-layout" style="display: flex; flex: 1; width: 100%;"', 'class="desktop-main-layout" style="display: flex; flex: 1; width: 100%; justify-content: center;"')

with open('index.html', 'w') as f:
    f.write(index_html)

print("Layout fixed.")
