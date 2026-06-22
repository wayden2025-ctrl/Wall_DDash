import re

# 1. Update index.html
with open('index.html', 'r') as f:
    idx_html = f.read()

# Restore original Play button
new_play_button = """<button onclick="window.location.href='game.html?v=1'" style="background: linear-gradient(45deg, #00ffff, #0088ff); color: #000; border: none; padding: 15px 40px; font-size: 24px; font-weight: bold; border-radius: 30px; cursor: pointer; text-transform: uppercase; font-family: 'Courier New', Courier, monospace; box-shadow: 0 0 20px rgba(0,255,255,0.6); transition: transform 0.2s, box-shadow 0.2s;">
                    Play
                </button>"""

idx_html = re.sub(r'<div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin-bottom: 20px;">.*?</div>', new_play_button, idx_html, flags=re.DOTALL)

# Remove Modal and Script
idx_html = re.sub(r'<!-- Customize Modal -->.*?</body>', '</body>', idx_html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(idx_html)

# 2. Update game.html
with open('game.html', 'r') as f:
    game_html = f.read()

customize_btn_html = """<button onclick="document.getElementById('customize-modal').style.display='flex';" style="background: transparent; border: 2px solid #00ffff; color: #00ffff; padding: 15px 20px; font-size: 20px; font-weight: bold; border-radius: 30px; cursor: pointer; text-transform: uppercase; font-family: 'Courier New', Courier, monospace; box-shadow: 0 0 10px rgba(0,255,255,0.3); transition: background 0.2s, color 0.2s; flex: 1;">CUSTOMIZE</button>"""

def inject_button(html, target_btn_id):
    pattern = rf'(<button id="{target_btn_id}"[^>]*>.*?</button>)'
    replacement = rf"""<div style="display: flex; gap: 10px; justify-content: center; margin-top: 15px; width: 100%;">
                    \1
                    {customize_btn_html}
                </div>"""
    return re.sub(pattern, replacement, html)

game_html = inject_button(game_html, "start-btn")
game_html = inject_button(game_html, "restart-btn")
game_html = inject_button(game_html, "win-restart-btn")

# If buttons lack flex: 1, they might look cramped. We will add flex: 1 to them using JS or directly.
# Let's add flex: 1 to those buttons using replace
game_html = game_html.replace('id="start-btn"', 'id="start-btn" style="flex: 1;"')
game_html = game_html.replace('id="restart-btn"', 'id="restart-btn" style="flex: 1;"')
game_html = game_html.replace('id="win-restart-btn"', 'id="win-restart-btn" style="flex: 1;"')

# Add modal to game.html
modal_html = """
    <!-- Customize Modal -->
    <div id="customize-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(5,5,8,0.95); z-index: 9999; flex-direction: column; align-items: center; justify-content: center; font-family: 'Courier New', Courier, monospace;">
        <h2 style="color: #00ffff; margin-bottom: 30px; font-size: 32px; text-shadow: 0 0 10px #00ffff;">Select Your Core</h2>
        
        <div id="orb-carousel" style="display: flex; gap: 30px; overflow-x: auto; scroll-snap-type: x mandatory; padding: 30px; max-width: 90vw; width: 600px; border: 2px solid rgba(0,255,255,0.5); border-radius: 20px; background: rgba(0,255,255,0.05); box-shadow: 0 0 40px rgba(0,255,255,0.1);">
            <!-- Orbs will be dynamically injected here via JS -->
        </div>
        
        <p id="orb-name" style="color: #fff; font-size: 28px; font-weight: bold; margin-top: 30px; text-transform: uppercase;">Default Neon</p>
        
        <button onclick="document.getElementById('customize-modal').style.display='none';" style="margin-top: 40px; background: #111; border: 2px solid #ff00ff; color: #ff00ff; padding: 15px 50px; font-size: 24px; border-radius: 30px; cursor: pointer; text-transform: uppercase; font-weight: bold; box-shadow: 0 0 20px rgba(255,0,255,0.4);">CONFIRM</button>
    </div>

    <script>
    const orbs = [
        { id: 0, name: 'Default Neon', color: '#00ffff', src: 'none' },
        { id: 1, name: 'Azure Core', color: '#0088ff', src: 'orb_1.png' },
        { id: 2, name: 'Crimson Eye', color: '#ff2222', src: 'orb_2.png' },
        { id: 3, name: 'Emerald Reactor', color: '#22ff22', src: 'orb_3.png' },
        { id: 4, name: 'Amethyst Void', color: '#8822ff', src: 'orb_4.png' },
        { id: 5, name: 'Solar Flare', color: '#ffff22', src: 'orb_5.png' },
        { id: 6, name: 'Molten Core', color: '#ff8822', src: 'orb_6.png' },
        { id: 7, name: 'Cyan Pulse', color: '#22ffff', src: 'orb_7.png' },
        { id: 8, name: 'Magenta Spark', color: '#ff22ff', src: 'orb_8.png' },
        { id: 9, name: 'Platinum Star', color: '#ffffff', src: 'orb_9.png' },
    ];

    function initCustomize() {
        const carousel = document.getElementById('orb-carousel');
        const nameLabel = document.getElementById('orb-name');
        let selectedId = parseInt(localStorage.getItem('selectedOrbId') || '0', 10);
        
        orbs.forEach(orb => {
            const item = document.createElement('div');
            item.style.cssText = 'flex: 0 0 auto; scroll-snap-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; padding: 15px; border-radius: 15px; transition: all 0.3s ease; width: 120px; height: 120px;';
            
            let visual;
            if (orb.id === 0) {
                visual = document.createElement('div');
                visual.style.cssText = 'width: 80px; height: 80px; border-radius: 50%; background: transparent; border: 15px solid #00ffff; box-shadow: 0 0 20px #00ffff, inset 0 0 20px #00ffff;';
            } else {
                visual = document.createElement('img');
                visual.src = orb.src;
                visual.style.cssText = 'width: 100px; height: 100px; filter: drop-shadow(0 0 15px ' + orb.color + ');';
            }
            
            if (orb.id === selectedId) {
                item.style.background = 'rgba(255,255,255,0.15)';
                item.style.transform = 'scale(1.15)';
                item.style.boxShadow = '0 0 20px ' + orb.color;
                nameLabel.textContent = orb.name;
                nameLabel.style.color = orb.color;
                nameLabel.style.textShadow = '0 0 15px ' + orb.color;
            }
            
            item.onclick = () => {
                localStorage.setItem('selectedOrbId', orb.id);
                localStorage.setItem('selectedOrbColor', orb.color);
                selectedId = orb.id;
                
                // visually update all
                Array.from(carousel.children).forEach((child, idx) => {
                    child.style.background = idx === selectedId ? 'rgba(255,255,255,0.15)' : 'transparent';
                    child.style.transform = idx === selectedId ? 'scale(1.15)' : 'scale(1)';
                    child.style.boxShadow = idx === selectedId ? '0 0 20px ' + orb.color : 'none';
                });
                nameLabel.textContent = orb.name;
                nameLabel.style.color = orb.color;
                nameLabel.style.textShadow = '0 0 15px ' + orb.color;
                
                item.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
                
                // Update live in game!
                if (window.updateOrbSelection) {
                    window.updateOrbSelection(orb.id, orb.color, orb.src);
                }
            };
            
            item.appendChild(visual);
            carousel.appendChild(item);
        });
    }
    setTimeout(initCustomize, 100);
    </script>
</body>"""

game_html = game_html.replace('</body>', modal_html)
with open('game.html', 'w') as f:
    f.write(game_html)


# 3. Update game.js
with open('game.js', 'r') as f:
    game_js = f.read()

# Expose updateOrbSelection function
orb_fn = """
window.updateOrbSelection = function(id, color, src) {
    selectedOrbId = id;
    selectedOrbColor = color;
    if (id > 0) {
        customOrbImage = new Image();
        customOrbImage.src = src;
    } else {
        customOrbImage = null;
    }
};
"""

if 'window.updateOrbSelection' not in game_js:
    game_js = game_js.replace("// --- Orb Customization ---", "// --- Orb Customization ---\n" + orb_fn)

with open('game.js', 'w') as f:
    f.write(game_js)

print("Moved Customize feature to game.html successfully.")
