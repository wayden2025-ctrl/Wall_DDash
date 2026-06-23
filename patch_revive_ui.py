import re

with open('game.html', 'r') as f:
    html = f.read()

# Add the Revive button inside the game-over-screen
old_btn_group = r"""<div style="display: flex; gap: 10px; justify-content: center; margin-top: 15px; width: 100%;">
                    <button id="restart-btn" style="flex: 1;">RESTART \(Space\)</button>
                    <button onclick="document.getElementById\('customize-modal'\).style.display='flex';" style="background: transparent; border: 2px solid #00ffff; color: #00ffff; padding: 15px 20px; font-size: 20px; font-weight: bold; border-radius: 30px; cursor: pointer; text-transform: uppercase; font-family: 'Courier New', Courier, monospace; box-shadow: 0 0 10px rgba\(0,255,255,0.3\); transition: background 0.2s, color 0.2s; flex: 1;">CUSTOMIZE</button>"""

new_btn_group = """<button id="revive-btn" onclick="revivePlayer()" style="background: linear-gradient(45deg, #00ffaa, #0088ff); border: none; color: #fff; padding: 20px 40px; font-size: 28px; font-weight: bold; border-radius: 30px; cursor: pointer; text-transform: uppercase; font-family: 'Courier New', Courier, monospace; box-shadow: 0 0 20px rgba(0,255,170,0.6); transition: transform 0.2s; width: 100%; margin-top: 20px; margin-bottom: 15px;" onmouseover="this.style.transform='scale(1.05)';" onmouseout="this.style.transform='scale(1)';">
                    REVIVE (3 Left)
                </button>
                <div style="display: flex; gap: 10px; justify-content: center; width: 100%;">
                    <button id="restart-btn" style="flex: 1;">RESTART (Space)</button>
                    <button onclick="document.getElementById('customize-modal').style.display='flex';" style="background: transparent; border: 2px solid #00ffff; color: #00ffff; padding: 15px 20px; font-size: 20px; font-weight: bold; border-radius: 30px; cursor: pointer; text-transform: uppercase; font-family: 'Courier New', Courier, monospace; box-shadow: 0 0 10px rgba(0,255,255,0.3); transition: background 0.2s, color 0.2s; flex: 1;">CUSTOMIZE</button>"""

html = re.sub(old_btn_group, new_btn_group, html)

with open('game.html', 'w') as f:
    f.write(html)
print("game.html patched with revive button.")
