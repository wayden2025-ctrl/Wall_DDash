import re

old_card = r"""            <!-- Card 1: Elite Core Bundle -->
            <div style="background: rgba\(20,20,30,0\.8\); border: 2px solid #00ffff; border-radius: 15px; padding: 30px; width: 340px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 0 20px rgba\(0,255,255,0\.2\);">
                <img src="store_title\.png" style="width: 100%; margin-bottom: 20px; animation: rainbowGlow 3s linear infinite;">
                <div style="display: grid; grid-template-columns: repeat\(3, 1fr\); gap: 10px; margin-bottom: 20px;">
                    <img src="premium_orb_10\.png" style="width: 60px; height: 60px; filter: drop-shadow\(0 0 5px #fff\);">
                    <img src="premium_orb_11\.png" style="width: 60px; height: 60px; filter: drop-shadow\(0 0 5px #fff\);">
                    <img src="premium_orb_12\.png" style="width: 60px; height: 60px; filter: drop-shadow\(0 0 5px #fff\);">
                    <img src="premium_orb_13\.png" style="width: 60px; height: 60px; filter: drop-shadow\(0 0 5px #fff\);">
                    <img src="premium_orb_14\.png" style="width: 60px; height: 60px; filter: drop-shadow\(0 0 5px #fff\);">
                    <img src="premium_orb_15\.png" style="width: 60px; height: 60px; filter: drop-shadow\(0 0 5px #fff\);">
                    <img src="premium_orb_16\.png" style="width: 60px; height: 60px; filter: drop-shadow\(0 0 5px #fff\);">
                    <img src="premium_orb_17\.png" style="width: 60px; height: 60px; filter: drop-shadow\(0 0 5px #fff\);">
                    <img src="premium_orb_18\.png" style="width: 60px; height: 60px; filter: drop-shadow\(0 0 5px #fff\);">
                </div>
                <h3 style="color: #00ffff; font-size: 24px; margin-bottom: 10px; text-align: center;">Elite Core Bundle</h3>
                <p style="color: #aaa; text-align: center; margin-bottom: 20px; min-height: 40px; line-height: 1\.4;">Unlocks 9 exclusive neon orb designs!</p>
                <button onclick="window\.location\.href='https://buy\.stripe\.com/test_5kQ00c2wtfkYcQHgS42wU00'" style="width: 100%; background: linear-gradient\(45deg, #00ffff, #0088ff\); color: #fff; border: none; padding: 15px; font-size: 20px; font-weight: bold; border-radius: 10px; cursor: pointer; box-shadow: 0 0 15px rgba\(0,255,255,0\.4\); transition: transform 0\.2s; margin-top: auto;" onmouseover="this\.style\.transform='scale\(1\.05\)';" onmouseout="this\.style\.transform='scale\(1\)';">
                    BUY \$1\.99
                </button>
            </div>"""

new_card = """            <!-- Card 1: Elite Core Bundle (Featured) -->
            <div style="background: rgba(20,20,30,0.8); border: 2px solid #00ffff; border-radius: 15px; padding: 40px; width: 100%; max-width: 710px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 0 30px rgba(0,255,255,0.3);">
                <img src="store_title.png" style="width: 80%; margin-bottom: 30px; animation: rainbowGlow 3s linear infinite;">
                <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; margin-bottom: 30px;">
                    <img src="premium_orb_10.png" style="width: 80px; height: 80px; filter: drop-shadow(0 0 5px #fff);">
                    <img src="premium_orb_11.png" style="width: 80px; height: 80px; filter: drop-shadow(0 0 5px #fff);">
                    <img src="premium_orb_12.png" style="width: 80px; height: 80px; filter: drop-shadow(0 0 5px #fff);">
                    <img src="premium_orb_13.png" style="width: 80px; height: 80px; filter: drop-shadow(0 0 5px #fff);">
                    <img src="premium_orb_14.png" style="width: 80px; height: 80px; filter: drop-shadow(0 0 5px #fff);">
                    <img src="premium_orb_15.png" style="width: 80px; height: 80px; filter: drop-shadow(0 0 5px #fff);">
                    <img src="premium_orb_16.png" style="width: 80px; height: 80px; filter: drop-shadow(0 0 5px #fff);">
                    <img src="premium_orb_17.png" style="width: 80px; height: 80px; filter: drop-shadow(0 0 5px #fff);">
                    <img src="premium_orb_18.png" style="width: 80px; height: 80px; filter: drop-shadow(0 0 5px #fff);">
                </div>
                <h3 style="color: #00ffff; font-size: 32px; margin-bottom: 15px; text-align: center;">Elite Core Bundle</h3>
                <p style="color: #aaa; text-align: center; font-size: 20px; margin-bottom: 30px; line-height: 1.4;">Unlocks 9 exclusive high-velocity neon orb designs!</p>
                <button onclick="window.location.href='https://buy.stripe.com/test_5kQ00c2wtfkYcQHgS42wU00'" style="width: 100%; max-width: 400px; background: linear-gradient(45deg, #00ffff, #0088ff); color: #fff; border: none; padding: 20px; font-size: 24px; font-weight: bold; border-radius: 15px; cursor: pointer; box-shadow: 0 0 20px rgba(0,255,255,0.5); transition: transform 0.2s; margin-top: auto;" onmouseover="this.style.transform='scale(1.05)';" onmouseout="this.style.transform='scale(1)';">
                    BUY $1.99
                </button>
            </div>"""

for file in ['index.html', 'game.html']:
    with open(file, 'r') as f:
        html = f.read()
    
    html = re.sub(old_card, new_card, html)
    
    with open(file, 'w') as f:
        f.write(html)
print("Updated Elite Core Bundle to be larger and featured on top.")
