import re

with open('index.html', 'r') as f:
    html = f.read()

# Replace the single PLAY button with a row of buttons
old_btn = r'<button onclick="window.location.href=\'game.html\?v=1\'" style="(.*?)">(.*?)</button>'
# Wait, maybe v=1 is updated. Let's just find the Play button.
old_btn_match = re.search(r'<button onclick="window.location.href=\'game.html\?v=\d+\'" style=".*?">\s*Play\s*</button>', html, flags=re.DOTALL)
if old_btn_match:
    play_btn = old_btn_match.group(0)
    
    new_btns = f"""
    <div style="display: flex; gap: 20px; justify-content: center; margin-top: 20px;">
        {play_btn}
        <button onclick="document.getElementById('store-modal').style.display='flex';" style="background: linear-gradient(45deg, #ffaa00, #ff0055); color: #fff; border: none; padding: 15px 40px; font-size: 24px; font-weight: bold; border-radius: 30px; cursor: pointer; text-transform: uppercase; font-family: 'Courier New', Courier, monospace; box-shadow: 0 0 20px rgba(255,170,0,0.6); transition: transform 0.2s, box-shadow 0.2s;" onmouseover="this.style.transform='scale(1.05)';" onmouseout="this.style.transform='scale(1)';">
            STORE
        </button>
    </div>
    """
    html = html.replace(play_btn, new_btns)

# Add the store modal before the closing </body> tag
store_modal = """
    <!-- Store Modal -->
    <div id="store-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(5,5,8,0.98); z-index: 10000; flex-direction: column; align-items: center; justify-content: center; font-family: 'Courier New', Courier, monospace; text-align: center;">
        <h2 style="color: #ffaa00; margin-bottom: 10px; font-size: 42px; text-shadow: 0 0 20px #ffaa00; text-transform: uppercase;">Elite Core Bundle</h2>
        <p style="color: #fff; font-size: 18px; max-width: 600px; margin-bottom: 30px;">Unlock 9 hyper-charged premium cores with exclusive high-velocity particle trails.</p>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 40px; background: rgba(255,170,0,0.05); padding: 20px; border-radius: 15px; border: 1px solid rgba(255,170,0,0.3); box-shadow: inset 0 0 30px rgba(255,170,0,0.1);">
            <img src="premium_orb_10.png" style="width: 80px; height: 80px; filter: drop-shadow(0 0 10px #0088ff);">
            <img src="premium_orb_11.png" style="width: 80px; height: 80px; filter: drop-shadow(0 0 10px #ff2222);">
            <img src="premium_orb_12.png" style="width: 80px; height: 80px; filter: drop-shadow(0 0 10px #22ff22);">
            <img src="premium_orb_13.png" style="width: 80px; height: 80px; filter: drop-shadow(0 0 10px #8822ff);">
            <img src="premium_orb_14.png" style="width: 80px; height: 80px; filter: drop-shadow(0 0 10px #ffff22);">
            <img src="premium_orb_15.png" style="width: 80px; height: 80px; filter: drop-shadow(0 0 10px #ff8822);">
            <img src="premium_orb_16.png" style="width: 80px; height: 80px; filter: drop-shadow(0 0 10px #22ffff);">
            <img src="premium_orb_17.png" style="width: 80px; height: 80px; filter: drop-shadow(0 0 10px #ff22ff);">
            <img src="premium_orb_18.png" style="width: 80px; height: 80px; filter: drop-shadow(0 0 10px #ffffff);">
        </div>

        <div id="checkout-container" style="display: flex; gap: 20px;">
            <button id="buy-btn" onclick="processPurchase()" style="background: linear-gradient(45deg, #ffaa00, #ff0055); color: #fff; border: none; padding: 15px 40px; font-size: 24px; font-weight: bold; border-radius: 30px; cursor: pointer; text-transform: uppercase; font-family: 'Courier New', Courier, monospace; box-shadow: 0 0 20px rgba(255,170,0,0.6); transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.05)';" onmouseout="this.style.transform='scale(1)';">
                Buy for $1.99
            </button>
            <button onclick="document.getElementById('store-modal').style.display='none';" style="background: transparent; color: #aaa; border: 2px solid #555; padding: 15px 40px; font-size: 24px; font-weight: bold; border-radius: 30px; cursor: pointer; text-transform: uppercase; font-family: 'Courier New', Courier, monospace; transition: all 0.2s;" onmouseover="this.style.color='#fff'; this.style.borderColor='#fff';" onmouseout="this.style.color='#aaa'; this.style.borderColor='#555';">
                Close
            </button>
        </div>

        <div id="processing-msg" style="display: none; color: #00ffff; font-size: 24px; text-shadow: 0 0 15px #00ffff; margin-top: 20px;">
            Processing secure transaction...
        </div>
        <div id="success-msg" style="display: none; color: #22ff22; font-size: 28px; text-shadow: 0 0 15px #22ff22; margin-top: 20px; font-weight: bold;">
            PURCHASE SUCCESSFUL! Bundle Unlocked.
        </div>
    </div>

    <script>
        function processPurchase() {
            document.getElementById('checkout-container').style.display = 'none';
            document.getElementById('processing-msg').style.display = 'block';
            
            // Simulate 1.5s transaction
            setTimeout(() => {
                document.getElementById('processing-msg').style.display = 'none';
                document.getElementById('success-msg').style.display = 'block';
                localStorage.setItem('premiumBundleUnlocked', 'true');
                
                // Auto close after 2 seconds
                setTimeout(() => {
                    document.getElementById('store-modal').style.display = 'none';
                    // Reset modal for future opens
                    document.getElementById('checkout-container').style.display = 'flex';
                    document.getElementById('success-msg').style.display = 'none';
                }, 2000);
            }, 1500);
        }
    </script>
</body>
"""

html = html.replace('</body>', store_modal)

with open('index.html', 'w') as f:
    f.write(html)
