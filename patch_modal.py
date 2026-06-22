import re

with open('game.html', 'r') as f:
    html = f.read()

# 1. Replace the modal-header h2
old_h2 = r'<h2 id="modal-header" .*?>Select Your Core</h2>'
new_h2 = r"""<h2 id="modal-header" style="position: relative; color: var(--theme-color, #00ffff); margin-bottom: 40px; margin-top: 20px; font-size: 42px; text-shadow: 0 0 15px var(--theme-color, #00ffff); transition: all 0.5s ease; border: 2px solid var(--theme-color, #00ffff); padding: 15px 50px; background: rgba(0,0,0,0.6); box-shadow: 0 0 20px var(--theme-color, #00ffff), inset 0 0 20px var(--theme-color, #00ffff); text-transform: uppercase;">
            <span style="position: absolute; top: -6px; left: -10px; width: 25px; height: 3px; background: var(--theme-color, #00ffff); box-shadow: 0 0 15px var(--theme-color, #00ffff);"></span>
            <span style="position: absolute; top: -6px; right: -10px; width: 25px; height: 3px; background: var(--theme-color, #00ffff); box-shadow: 0 0 15px var(--theme-color, #00ffff);"></span>
            <span style="position: absolute; bottom: -6px; left: -10px; width: 25px; height: 3px; background: var(--theme-color, #00ffff); box-shadow: 0 0 15px var(--theme-color, #00ffff);"></span>
            <span style="position: absolute; bottom: -6px; right: -10px; width: 25px; height: 3px; background: var(--theme-color, #00ffff); box-shadow: 0 0 15px var(--theme-color, #00ffff);"></span>
            <span style="position: absolute; top: 50%; left: -40px; width: 25px; height: 3px; background: var(--theme-color, #00ffff); box-shadow: 0 0 15px var(--theme-color, #00ffff); transform: translateY(-50%);"></span>
            <span style="position: absolute; top: 50%; right: -40px; width: 25px; height: 3px; background: var(--theme-color, #00ffff); box-shadow: 0 0 15px var(--theme-color, #00ffff); transform: translateY(-50%);"></span>
            Select Your Core
        </h2>"""
html = re.sub(old_h2, new_h2, html)

# 2. Enlarge carousel container
html = html.replace('width: 600px;', 'width: 1000px;')
html = html.replace('max-width: 90vw;', 'max-width: 95vw;')
html = html.replace('padding: 30px;', 'padding: 40px;')
html = html.replace('gap: 30px;', 'gap: 40px;')

# 3. Enlarge title container
html = html.replace('height: 100px;', 'height: 160px;')
html = html.replace('margin-top: 20px;', 'margin-top: 40px;')

# 4. Enlarge CONFIRM button
html = html.replace('padding: 15px 60px;', 'padding: 20px 80px;')
html = html.replace('font-size: 26px;', 'font-size: 34px;')
html = html.replace('margin-top: 40px;', 'margin-top: 60px;')

# 5. Enlarge individual orbs in the carousel
html = html.replace('width: 120px; height: 120px;', 'width: 180px; height: 180px;')
html = html.replace('width: 80px; height: 80px;', 'width: 120px; height: 120px;')
html = html.replace('border: 15px solid #00ffff;', 'border: 22px solid #00ffff;')
html = html.replace('width: 100px; height: 100px;', 'width: 150px; height: 150px;')

# 6. Update updateModalTheme() function to correctly color the new h2
old_theme = r"""            modalHeader\.style\.color = color;
            modalHeader\.style\.textShadow = '0 0 15px ' \+ color;"""
new_theme = r"""            modalHeader.style.setProperty('--theme-color', color);"""
html = re.sub(old_theme, new_theme, html)

# Bump version in game.html to ensure cache bust
html = re.sub(r'game\.js\?v=\d+', 'game.js?v=42', html)

with open('game.html', 'w') as f:
    f.write(html)

print("Applied sci-fi geometric styling to the modal header and enlarged the entire modal!")
