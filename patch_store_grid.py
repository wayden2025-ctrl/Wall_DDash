import re

new_store_modal = """    <!-- Store Modal -->
    <div id="store-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(5,5,8,0.95); z-index: 9999; flex-direction: column; align-items: center; justify-content: flex-start; overflow-y: auto; font-family: 'Courier New', Courier, monospace; transition: background 0.5s ease; padding: 40px 0;">
        <!-- Close Button Top Right -->
        <button onclick="document.getElementById('store-modal').style.display='none';" style="position: absolute; top: 20px; right: 30px; background: transparent; color: #fff; border: 2px solid #555; padding: 10px 20px; font-size: 18px; font-weight: bold; border-radius: 10px; cursor: pointer; text-transform: uppercase; transition: all 0.2s;" onmouseover="this.style.borderColor='#fff';" onmouseout="this.style.borderColor='#555';">CLOSE X</button>

        <!-- Title -->
        <h2 style="color: #fff; font-size: 48px; margin-bottom: 40px; text-shadow: 0 0 20px #ff00ff; text-align: center;">WALL DASH STORE</h2>
        
        <div id="checkout-container" style="display: flex; flex-wrap: wrap; gap: 30px; justify-content: center; max-width: 1200px; padding: 0 20px; margin-bottom: 40px;">
            
            <!-- Card 1: Elite Core Bundle -->
            <div style="background: rgba(20,20,30,0.8); border: 2px solid #00ffff; border-radius: 15px; padding: 30px; width: 340px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 0 20px rgba(0,255,255,0.2);">
                <img src="store_title.png" style="width: 100%; margin-bottom: 20px; animation: rainbowGlow 3s linear infinite;">
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 20px;">
                    <img src="premium_orb_10.png" style="width: 60px; height: 60px; filter: drop-shadow(0 0 5px #fff);">
                    <img src="premium_orb_11.png" style="width: 60px; height: 60px; filter: drop-shadow(0 0 5px #fff);">
                    <img src="premium_orb_12.png" style="width: 60px; height: 60px; filter: drop-shadow(0 0 5px #fff);">
                    <img src="premium_orb_13.png" style="width: 60px; height: 60px; filter: drop-shadow(0 0 5px #fff);">
                    <img src="premium_orb_14.png" style="width: 60px; height: 60px; filter: drop-shadow(0 0 5px #fff);">
                    <img src="premium_orb_15.png" style="width: 60px; height: 60px; filter: drop-shadow(0 0 5px #fff);">
                    <img src="premium_orb_16.png" style="width: 60px; height: 60px; filter: drop-shadow(0 0 5px #fff);">
                    <img src="premium_orb_17.png" style="width: 60px; height: 60px; filter: drop-shadow(0 0 5px #fff);">
                    <img src="premium_orb_18.png" style="width: 60px; height: 60px; filter: drop-shadow(0 0 5px #fff);">
                </div>
                <h3 style="color: #00ffff; font-size: 24px; margin-bottom: 10px; text-align: center;">Elite Core Bundle</h3>
                <p style="color: #aaa; text-align: center; margin-bottom: 20px; min-height: 40px; line-height: 1.4;">Unlocks 9 exclusive neon orb designs!</p>
                <button onclick="window.location.href='https://buy.stripe.com/test_5kQ00c2wtfkYcQHgS42wU00'" style="width: 100%; background: linear-gradient(45deg, #00ffff, #0088ff); color: #fff; border: none; padding: 15px; font-size: 20px; font-weight: bold; border-radius: 10px; cursor: pointer; box-shadow: 0 0 15px rgba(0,255,255,0.4); transition: transform 0.2s; margin-top: auto;" onmouseover="this.style.transform='scale(1.05)';" onmouseout="this.style.transform='scale(1)';">
                    BUY $1.99
                </button>
            </div>

            <!-- Card 2: 1x Revive -->
            <div style="background: rgba(20,20,30,0.8); border: 2px solid #ff0055; border-radius: 15px; padding: 30px; width: 340px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 0 20px rgba(255,0,85,0.2);">
                <img src="revive_logo.jpg" style="width: 180px; height: 180px; border-radius: 20px; margin-bottom: 20px; box-shadow: 0 0 20px #ff0055; object-fit: cover;">
                <h3 style="color: #ff0055; font-size: 28px; margin-bottom: 10px; text-align: center; text-shadow: 0 0 10px #ff0055;">1x Extra Life</h3>
                <p style="color: #aaa; text-align: center; margin-bottom: 20px; min-height: 40px; line-height: 1.4;">Resume playing exactly where you died.</p>
                <button onclick="window.location.href='https://buy.stripe.com/test_revive_1'" style="width: 100%; background: linear-gradient(45deg, #ffaa00, #ff0055); color: #fff; border: none; padding: 15px; font-size: 20px; font-weight: bold; border-radius: 10px; cursor: pointer; box-shadow: 0 0 15px rgba(255,0,85,0.4); transition: transform 0.2s; margin-top: auto;" onmouseover="this.style.transform='scale(1.05)';" onmouseout="this.style.transform='scale(1)';">
                    BUY $1.00
                </button>
            </div>

            <!-- Card 3: 3x Revive -->
            <div style="background: rgba(30,20,20,0.9); border: 3px solid #ffaa00; border-radius: 15px; padding: 30px; width: 340px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 0 30px rgba(255,170,0,0.4); position: relative;">
                <div style="position: absolute; top: -15px; background: #ffaa00; color: #000; font-weight: bold; padding: 8px 20px; border-radius: 10px; font-size: 16px; box-shadow: 0 0 10px #ffaa00;">BEST VALUE</div>
                <img src="revive_logo.jpg" style="width: 180px; height: 180px; border-radius: 20px; margin-bottom: 20px; box-shadow: 0 0 30px #ffaa00; object-fit: cover;">
                <h3 style="color: #ffaa00; font-size: 28px; margin-bottom: 10px; text-align: center; text-shadow: 0 0 10px #ffaa00;">3x Extra Lives</h3>
                <p style="color: #aaa; text-align: center; margin-bottom: 20px; min-height: 40px; line-height: 1.4;">Stack up on revives to beat your high score!</p>
                <button onclick="window.location.href='https://buy.stripe.com/test_revive_3'" style="width: 100%; background: linear-gradient(45deg, #ffff00, #ffaa00); color: #000; border: none; padding: 15px; font-size: 20px; font-weight: bold; border-radius: 10px; cursor: pointer; box-shadow: 0 0 15px rgba(255,170,0,0.4); transition: transform 0.2s; margin-top: auto;" onmouseover="this.style.transform='scale(1.05)';" onmouseout="this.style.transform='scale(1)';">
                    BUY $2.00
                </button>
            </div>
            
        </div>

        <div id="processing-msg" style="display: none; color: #00ffff; font-size: 24px; text-shadow: 0 0 15px #00ffff; margin-top: 40px; text-align: center;">
            Processing secure transaction...
        </div>
        <div id="success-msg" style="display: none; color: #22ff22; font-size: 28px; text-shadow: 0 0 15px #22ff22; margin-top: 40px; font-weight: bold; text-align: center;">
            PURCHASE SUCCESSFUL!<br><span style="font-size: 18px; color: #ccc;">Close the store to resume playing.</span>
        </div>
    </div>"""

# Replace the modal in both files
for file in ['index.html', 'game.html']:
    with open(file, 'r') as f:
        html = f.read()
    
    html = re.sub(r'<!-- Store Modal -->.*?</div>\s*</div>\s*</div>', new_store_modal, html, flags=re.DOTALL)
    
    # Also update the success handlers
    old_handler = r"""if \(urlParams\.get\('revive_success'\) === 'true'\) \{.*?window\.history\.replaceState\(\{\}, document\.title, window\.location\.pathname\);\s+\}"""
    
    new_handler = """const reviveSuccess = urlParams.get('revive_success');
            if (reviveSuccess) {
                let currentRevives = parseInt(localStorage.getItem('revivesLeft')) || 0;
                const count = parseInt(reviveSuccess);
                if (!isNaN(count)) {
                    localStorage.setItem('revivesLeft', (currentRevives + count).toString());
                    document.getElementById('store-modal').style.display = 'flex';
                    const cm = document.getElementById('checkout-container');
                    if(cm) cm.style.display = 'none';
                    const sm = document.getElementById('success-msg');
                    if(sm) {
                        sm.innerHTML = `PURCHASE SUCCESSFUL!<br><span style="font-size: 18px; color: #ccc;">+${count} Revives added to your account! Close the store to resume playing.</span>`;
                        sm.style.display = 'block';
                    }
                }
                window.history.replaceState({}, document.title, window.location.pathname);
            }"""
            
    html = re.sub(old_handler, new_handler, html, flags=re.DOTALL)
    
    with open(file, 'w') as f:
        f.write(html)

print("Store modal updated with grid layout in index.html and game.html.")
