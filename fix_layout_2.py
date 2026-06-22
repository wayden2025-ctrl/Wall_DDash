import re

def fix_html(filepath):
    with open(filepath, 'r') as f:
        html = f.read()

    # Make sidebars truly equal
    html = re.sub(r'class="ad-space-desktop left-ad"', 'class="ad-space-desktop left-ad" style="flex: 1 1 0; min-width: 0;"', html)
    html = re.sub(r'class="ad-space-desktop right-ad"', 'class="ad-space-desktop right-ad" style="flex: 1 1 0; min-width: 0;"', html)
    
    # Fix the footer so it centers
    html = html.replace('class="site-footer" style="margin-top: auto; width: 100%; max-width: 800px;"', 'class="site-footer" style="margin-top: auto; width: 100%; max-width: 800px; margin-left: auto; margin-right: auto;"')
    
    # Also fix index.html footer which might not have inline style
    html = html.replace('<footer class="site-footer">', '<footer class="site-footer" style="margin: auto auto 0 auto; width: 100%; max-width: 800px;">')
    
    # game.html specific fix: The game-container wrapper
    html = html.replace('<div style="flex: 0 1 600px; max-width: 600px; width: 100%; height: 100%; position: relative;">', '<div style="flex: 0 0 600px; width: 100%; height: 100%; position: relative;">')

    with open(filepath, 'w') as f:
        f.write(html)

fix_html('game.html')
fix_html('index.html')

print("Fixed.")
