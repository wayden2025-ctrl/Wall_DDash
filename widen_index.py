with open('index.html', 'r') as f:
    html = f.read()

# 1. Left sidebar
html = html.replace(
    'class="ad-space-desktop left-ad" style="flex: 1 1 0; min-width: 0; max-width: calc(50vw - 300px);"',
    'class="ad-space-desktop left-ad" style="flex: 1 1 0; min-width: 0; max-width: calc(50vw - 450px);"'
)

# 2. Right sidebar
html = html.replace(
    'class="ad-space-desktop right-ad" style="flex: 1 1 0; min-width: 0; max-width: calc(50vw - 300px);"',
    'class="ad-space-desktop right-ad" style="flex: 1 1 0; min-width: 0; max-width: calc(50vw - 450px);"'
)

# 3. Center container
html = html.replace(
    '<div style="flex: 1 1 100%; max-width: 600px; width: 100%;">',
    '<div style="flex: 1 1 100%; max-width: 900px; width: 100%;">'
)

# 4. Glass-panel
html = html.replace(
    'max-width: 600px; padding: 40px; display: flex;',
    'max-width: 900px; padding: 40px; display: flex;'
)

# 5. Publisher content
html = html.replace(
    'max-width: 800px; margin: 40px auto;',
    'max-width: 900px; margin: 40px auto;'
)

with open('index.html', 'w') as f:
    f.write(html)
print("index.html widened.")
