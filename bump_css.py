import re

for file in ['index.html', 'game.html']:
    with open(file, 'r') as f:
        html = f.read()
    html = re.sub(r'style\.css\?v=\d+', 'style.css?v=25', html)
    html = re.sub(r'game\.js\?v=\d+', 'game.js?v=25', html)
    with open(file, 'w') as f:
        f.write(html)
print("Bumped.")
