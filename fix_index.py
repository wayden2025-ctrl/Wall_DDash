import re

with open('index.html', 'r') as f:
    html = f.read()

# Make the sidebars perfectly balanced
html = re.sub(
    r'class="ad-space-desktop left-ad" style="[^"]*"',
    r'class="ad-space-desktop left-ad" style="flex: 1 1 0; min-width: 0; max-width: calc(50vw - 300px);"',
    html
)
html = re.sub(
    r'class="ad-space-desktop right-ad" style="[^"]*"',
    r'class="ad-space-desktop right-ad" style="flex: 1 1 0; min-width: 0; max-width: calc(50vw - 300px);"',
    html
)

# Fix the main layout to justify center
html = html.replace(
    'class="desktop-main-layout" style="display: flex; flex: 1; width: 100%;"',
    'class="desktop-main-layout" style="display: flex; flex: 1; width: 100%; justify-content: center;"'
)

# Center the footer
html = html.replace(
    '<footer class="site-footer">',
    '<footer class="site-footer" style="margin-top: auto; width: 100%; max-width: 800px; margin-left: auto; margin-right: auto; text-align: center;">'
)

# And add margin: 0 auto to the glass-panel just in case
html = html.replace(
    'class="glass-panel"',
    'class="glass-panel" style="margin: 0 auto;"'
)
# Wait, glass-panel might already have style
html = re.sub(
    r'class="glass-panel" style="',
    r'class="glass-panel" style="margin: 0 auto; ',
    html
)

with open('index.html', 'w') as f:
    f.write(html)
print("index.html fixed.")
