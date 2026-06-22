import re

with open('game.js', 'r') as f:
    js = f.read()

# Remove the old player image loader
js = js.replace("const playerImage = new Image();\nplayerImage.src = 'player.png';", "")

orb_init = """// --- Orb Customization ---
let selectedOrbId = parseInt(localStorage.getItem('selectedOrbId') || '0', 10);
let selectedOrbColor = localStorage.getItem('selectedOrbColor') || '#00ffff';
let customOrbImage = null;

if (selectedOrbId > 0) {
    customOrbImage = new Image();
    customOrbImage.src = 'orb_' + selectedOrbId + '.png';
}
"""

if '// --- Orb Customization ---' not in js:
    js = js.replace("// UI Elements", orb_init + "\n// UI Elements")
    print("Added orb_init")

with open('game.js', 'w') as f:
    f.write(js)
