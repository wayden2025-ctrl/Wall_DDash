import re

# 1. Update game.html to add STORE button to the start/pause/gameover menus
with open('game.html', 'r') as f:
    html = f.read()

store_btn_html = r"""<button onclick="window.location.href='https://buy.stripe.com/test_5kQ00c2wtfkYcQHgS42wU00'" style="background: linear-gradient(45deg, #ffaa00, #ff0055); border: none; color: #fff; padding: 15px 20px; font-size: 20px; font-weight: bold; border-radius: 30px; cursor: pointer; text-transform: uppercase; font-family: 'Courier New', Courier, monospace; box-shadow: 0 0 10px rgba(255,170,0,0.5); transition: transform 0.2s; flex: 1;" onmouseover="this.style.transform='scale(1.05)';" onmouseout="this.style.transform='scale(1)';">STORE</button>"""

# Find all Customize buttons and append the Store button after them
old_customize = r'(<button onclick="document\.getElementById\(\'customize-modal\'\)\.style\.display=\'flex\';".*?>CUSTOMIZE</button>)'
html = re.sub(old_customize, r'\1\n                    ' + store_btn_html, html)

with open('game.html', 'w') as f:
    f.write(html)

# 2. Update index.html to add rainbow glow to store_title.png
with open('index.html', 'r') as f:
    html_index = f.read()

# Add keyframes before closing </style>
if "rainbowGlow" not in html_index:
    keyframes = """
        @keyframes rainbowGlow {
            0% { filter: drop-shadow(0 0 20px #ff0000); }
            16% { filter: drop-shadow(0 0 20px #ffaa00); }
            33% { filter: drop-shadow(0 0 20px #ffff00); }
            50% { filter: drop-shadow(0 0 20px #00ff00); }
            66% { filter: drop-shadow(0 0 20px #0000ff); }
            83% { filter: drop-shadow(0 0 20px #aa00ff); }
            100% { filter: drop-shadow(0 0 20px #ff0000); }
        }
    </style>"""
    html_index = html_index.replace("</style>", keyframes, 1)

# Apply animation to image
old_img = r'<img src="store_title\.png" style=".*?">'
new_img = r'<img src="store_title.png" style="width: 90%; max-width: 900px; margin-bottom: 20px; animation: rainbowGlow 3s linear infinite;">'
html_index = re.sub(old_img, new_img, html_index)

with open('index.html', 'w') as f:
    f.write(html_index)

print("game.html and index.html patched with rainbow glow and store buttons.")
