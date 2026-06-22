import re

ad_snippet = """<ins class="adsbygoogle"
                 style="display:block"
                 data-ad-client="ca-pub-6859171401389344"
                 data-ad-slot="2448522751"
                 data-ad-format="auto"
                 data-full-width-responsive="true"></ins>
            <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>"""

# Fix index.html
with open('index.html', 'r') as f:
    html = f.read()

html = re.sub(
    r'<div class="ad-space-desktop right-ad" style="([^"]+)"></div>',
    f'<div class="ad-space-desktop right-ad" style="\\1">\n            {ad_snippet}\n        </div>',
    html
)

with open('index.html', 'w') as f:
    f.write(html)

# Fix game.html
with open('game.html', 'r') as f:
    html = f.read()

html = re.sub(
    r'<div class="ad-space-desktop right-ad" style="([^"]+)"></div>',
    f'<div class="ad-space-desktop right-ad" style="\\1">\n            {ad_snippet}\n        </div>',
    html
)

with open('game.html', 'w') as f:
    f.write(html)

print("Right ads added.")
