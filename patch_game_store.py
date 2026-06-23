import re

with open('game.html', 'r') as f:
    html = f.read()

# Add a flex wrapper to confirm-btn and a new Store button
old_btn_match = re.search(r'(<button id="confirm-btn".*?>.*?CONFIRM.*?</button>)', html, flags=re.DOTALL)
if old_btn_match:
    confirm_btn = old_btn_match.group(1)
    
    # Check if we already wrapped it previously
    if "div style=\"display: flex" not in html:
        new_btns = f"""
        <div style="display: flex; gap: 30px; justify-content: center; align-items: center; margin-top: 60px;">
            <button onclick="window.location.href='https://buy.stripe.com/test_5kQ00c2wtfkYcQHgS42wU00'" style="position: relative; background: linear-gradient(45deg, #ffaa00, #ff0055); border: none; color: #fff; padding: 20px 80px; font-size: 34px; border-radius: 4px; cursor: pointer; text-transform: uppercase; font-family: 'Courier New', Courier, monospace; font-weight: bold; box-shadow: 0 0 20px rgba(255,170,0,0.6); transition: all 0.3s ease; text-shadow: 0 0 8px #fff; z-index: 1;" onmouseover="this.style.transform='scale(1.05)';" onmouseout="this.style.transform='scale(1)';">
                STORE
            </button>
            {confirm_btn.replace('margin-top: 60px;', '')}
        </div>
        """
        html = html.replace(confirm_btn, new_btns)

with open('game.html', 'w') as f:
    f.write(html)
print("game.html patched with STORE button.")
