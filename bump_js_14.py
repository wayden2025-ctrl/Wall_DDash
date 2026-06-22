import re
with open('index.html', 'r') as f: html = f.read()
html = re.sub(r'game\.js\?v=\d+', 'game.js?v=42', html)
with open('index.html', 'w') as f: f.write(html)
print("Bumped version to 42")
