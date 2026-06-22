import re

with open('index.html', 'r') as f:
    html = f.read()

# Fix the left ad space inline style
html = html.replace('<div class="ad-space-desktop left-ad">', '<div class="ad-space-desktop left-ad" style="flex: 0 0 320px;">')

# Ensure the landing container has more flex
html = html.replace('<div id="landing-container" style="flex: 1;', '<div id="landing-container" style="flex: 1 1 auto;')

# Add the right ad space
html = html.replace('</div>\n</body>', '</div>\n        <!-- Right spacer for balance -->\n        <div class="ad-space-desktop right-ad" style="flex: 0 0 320px;"></div>\n    </div>\n</body>')

with open('index.html', 'w') as f:
    f.write(html)
