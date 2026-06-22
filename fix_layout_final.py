import re

# Fix game.html
with open('game.html', 'r') as f:
    game_html = f.read()

# For the wrapper around game-container, we want it to be able to shrink!
game_html = re.sub(
    r'<div style="flex: [^"]*? position: relative;">\s*<div id="game-container"',
    '<div style="flex: 1 1 100%; max-width: 600px; width: 100%; height: 100%; position: relative;">\n            <div id="game-container"',
    game_html
)

# Fix footer in game.html to explicitly align center and take full width
game_html = re.sub(
    r'<footer class="site-footer"[^>]*>',
    '<footer class="site-footer" style="margin-top: auto; width: 100%; max-width: 800px; align-self: center; text-align: center;">',
    game_html
)

# Ad spaces: we want them to take available space but NOT squash the center container to 0
game_html = re.sub(
    r'class="ad-space-desktop left-ad"[^>]*>',
    'class="ad-space-desktop left-ad" style="flex: 1 1 auto;">',
    game_html
)

game_html = re.sub(
    r'class="ad-space-desktop right-ad"[^>]*>',
    'class="ad-space-desktop right-ad" style="flex: 1 1 auto;">',
    game_html
)

with open('game.html', 'w') as f:
    f.write(game_html)


# Fix index.html
with open('index.html', 'r') as f:
    index_html = f.read()

index_html = re.sub(
    r'class="ad-space-desktop left-ad"[^>]*>',
    'class="ad-space-desktop left-ad" style="flex: 1 1 auto;">',
    index_html
)
index_html = re.sub(
    r'class="ad-space-desktop right-ad"[^>]*>',
    'class="ad-space-desktop right-ad" style="flex: 1 1 auto;">',
    index_html
)
index_html = re.sub(
    r'<footer class="site-footer"[^>]*>',
    '<footer class="site-footer" style="margin-top: auto; width: 100%; max-width: 800px; align-self: center; text-align: center;">',
    index_html
)

# Update landing-container
index_html = re.sub(
    r'<div id="landing-container" style="flex: [^"]*">',
    '<div id="landing-container" style="flex: 1 1 100%; max-width: 800px; width: 100%; display: flex; flex-direction: column; align-items: center; text-align: center; overflow-y: auto; padding: 40px 20px;">',
    index_html
)

with open('index.html', 'w') as f:
    f.write(index_html)

print("Final fix applied.")
