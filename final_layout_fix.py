import re

for filepath in ['game.html', 'index.html']:
    with open(filepath, 'r') as f:
        html = f.read()

    # Make sidebars truly equal and completely balanced
    html = re.sub(r'class="ad-space-desktop left-ad" style="[^"]*"', r'class="ad-space-desktop left-ad" style="flex: 1 1 0; min-width: 0;"', html)
    html = re.sub(r'class="ad-space-desktop right-ad" style="[^"]*"', r'class="ad-space-desktop right-ad" style="flex: 1 1 0; min-width: 0;"', html)
    
    # Also explicitly add an empty block for the right ad just to make sure they're structurally balanced if needed (already there)

    # Make sure the logo is contained
    html = html.replace('max-width: 90%; max-height: 250px;', 'max-width: 100%; height: auto; max-height: 250px; object-fit: contain;')

    with open(filepath, 'w') as f:
        f.write(html)

print("Layout fixed permanently.")
