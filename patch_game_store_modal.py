import re

with open('index.html', 'r') as f:
    html_index = f.read()

with open('game.html', 'r') as f:
    html_game = f.read()

# 1. Extract the store modal and the rainbowGlow keyframes from index.html
modal_match = re.search(r'<!-- Store Modal -->.*?</div>\s*</div>\s*</div>', html_index, flags=re.DOTALL)
if not modal_match:
    # Just do a rough extraction
    modal_match = re.search(r'<!-- Store Modal -->.*?<div id="success-msg".*?</div>\s*</div>', html_index, flags=re.DOTALL)
    
store_modal = modal_match.group(0)

# Replace the button onclicks in game.html to open the modal
html_game = html_game.replace("window.location.href='https://buy.stripe.com/test_5kQ00c2wtfkYcQHgS42wU00'", "document.getElementById('store-modal').style.display='flex';")

# 2. Inject the store modal into game.html (before </body>)
if '<!-- Store Modal -->' not in html_game:
    html_game = html_game.replace('</body>', f'\n{store_modal}\n</body>')

# 3. Add rainbowGlow to game.html
if 'rainbowGlow' not in html_game:
    keyframes = """
    <style>
        @keyframes rainbowGlow {
            0% { filter: drop-shadow(0 0 20px #ff0000); }
            16% { filter: drop-shadow(0 0 20px #ffaa00); }
            33% { filter: drop-shadow(0 0 20px #ffff00); }
            50% { filter: drop-shadow(0 0 20px #00ff00); }
            66% { filter: drop-shadow(0 0 20px #0000ff); }
            83% { filter: drop-shadow(0 0 20px #aa00ff); }
            100% { filter: drop-shadow(0 0 20px #ff0000); }
        }
    </style>
</head>"""
    html_game = html_game.replace('</head>', keyframes)

with open('game.html', 'w') as f:
    f.write(html_game)

print("game.html patched to use local store modal.")
