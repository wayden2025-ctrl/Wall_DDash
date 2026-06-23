import re

with open('index.html', 'r') as f:
    html = f.read()

# Make grid images larger
html = re.sub(r'width:\s*80px;\s*height:\s*80px;', 'width: 130px; height: 130px;', html)
# Make modal title use the image
old_h2 = r'<h2.*?Elite Core Bundle.*?</h2>'
new_img = r'<img src="store_title.png" style="width: 90%; max-width: 900px; margin-bottom: 20px; filter: drop-shadow(0 0 20px rgba(255,170,0,0.5));">'
html = re.sub(old_h2, new_img, html)

# Make paragraph slightly bigger
html = re.sub(r'font-size:\s*18px;\s*max-width:\s*600px;', 'font-size: 22px; max-width: 800px;', html)

with open('index.html', 'w') as f:
    f.write(html)
    
print("index.html store size updated.")
