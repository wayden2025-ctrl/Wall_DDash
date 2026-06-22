import re

with open('game.html', 'r') as f:
    html = f.read()

# Replace the img tag with a highly styled button
# Use CSS variables --theme-color for dynamic coloring
old_img = r'<img id="confirm-btn" .*?>'
new_btn = r"""<button id="confirm-btn" onclick="document.getElementById('customize-modal').style.display='none';" style="position: relative; margin-top: 40px; background: rgba(0,0,0,0.8); border: 2px solid var(--theme-color, #ff00ff); color: var(--theme-color, #ff00ff); padding: 15px 60px; font-size: 26px; border-radius: 4px; cursor: pointer; text-transform: uppercase; font-family: 'Courier New', Courier, monospace; font-weight: bold; box-shadow: 0 0 15px var(--theme-color, #ff00ff), inset 0 0 15px var(--theme-color, #ff00ff); transition: all 0.3s ease; text-shadow: 0 0 8px var(--theme-color, #ff00ff); z-index: 1;" onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 0 30px var(--theme-color), inset 0 0 30px var(--theme-color)';" onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 0 15px var(--theme-color), inset 0 0 15px var(--theme-color)';">
    <span style="position: absolute; top: -6px; left: -10px; width: 20px; height: 2px; background: var(--theme-color); box-shadow: 0 0 10px var(--theme-color);"></span>
    <span style="position: absolute; top: -6px; right: -10px; width: 20px; height: 2px; background: var(--theme-color); box-shadow: 0 0 10px var(--theme-color);"></span>
    <span style="position: absolute; bottom: -6px; left: -10px; width: 20px; height: 2px; background: var(--theme-color); box-shadow: 0 0 10px var(--theme-color);"></span>
    <span style="position: absolute; bottom: -6px; right: -10px; width: 20px; height: 2px; background: var(--theme-color); box-shadow: 0 0 10px var(--theme-color);"></span>
    <span style="position: absolute; top: 50%; left: -30px; width: 20px; height: 2px; background: var(--theme-color); box-shadow: 0 0 10px var(--theme-color);"></span>
    <span style="position: absolute; top: 50%; right: -30px; width: 20px; height: 2px; background: var(--theme-color); box-shadow: 0 0 10px var(--theme-color);"></span>
    CONFIRM
</button>"""
html = re.sub(old_img, new_btn, html)

# Replace JS logic
old_js = r"            confirmBtn\.style\.filter = 'drop-shadow\(0 0 20px ' \+ color \+ '\)';?"
new_js = r"            confirmBtn.style.setProperty('--theme-color', color);"
html = re.sub(old_js, new_js, html)

with open('game.html', 'w') as f:
    f.write(html)
print("Reverted to a heavily styled CSS button!")
