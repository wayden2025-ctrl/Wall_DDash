import re

with open('game.html', 'r') as f:
    html = f.read()

# Replace HTML element
old_btn = r'<button id="confirm-btn" .*?>CONFIRM</button>'
new_btn = r"""<img id="confirm-btn" src="confirm_btn.png" onclick="document.getElementById('customize-modal').style.display='none';" style="margin-top: 30px; height: 70px; cursor: pointer; filter: drop-shadow(0 0 15px #ff00ff); transition: filter 0.5s ease, transform 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">"""
html = re.sub(old_btn, new_btn, html)

# Replace JS logic
old_js = r"""            confirmBtn\.style\.borderColor = color;
            confirmBtn\.style\.color = color;
            confirmBtn\.style\.boxShadow = '0 0 20px ' \+ color \+ '60';"""
new_js = r"""            confirmBtn.style.filter = 'drop-shadow(0 0 20px ' + color + ')';"""
html = re.sub(old_js, new_js, html)

with open('game.html', 'w') as f:
    f.write(html)
print("Replaced confirm button!")
