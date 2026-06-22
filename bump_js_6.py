import re
for file in ['index.html', 'game.html']:
    with open(file, 'r') as f: html = f.read()
    html = re.sub(r'game\.js\?v=\d+', 'game.js?v=34', html)
    with open(file, 'w') as f: f.write(html)
print("Bumped version to 34")
