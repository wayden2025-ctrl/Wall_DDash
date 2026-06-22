import re

with open('game.html', 'r') as f:
    html = f.read()

# Locate the customize-modal
pattern = r'(<!-- Customize Modal -->.*?</body>)'
match = re.search(pattern, html, flags=re.DOTALL)
if not match:
    print("Could not find modal block")
    exit(1)

new_modal_block = """<!-- Customize Modal -->
    <div id="customize-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(5,5,8,0.95); z-index: 9999; flex-direction: column; align-items: center; justify-content: center; font-family: 'Courier New', Courier, monospace; transition: background 0.5s ease;">
        <h2 id="modal-header" style="color: #00ffff; margin-bottom: 20px; font-size: 32px; text-shadow: 0 0 10px #00ffff; transition: color 0.5s ease, text-shadow 0.5s ease;">Select Your Core</h2>
        
        <div id="orb-carousel" style="display: flex; gap: 30px; overflow-x: auto; scroll-snap-type: x mandatory; padding: 30px; max-width: 90vw; width: 600px; border: 2px solid rgba(0,255,255,0.5); border-radius: 20px; background: rgba(0,255,255,0.05); box-shadow: 0 0 40px rgba(0,255,255,0.1); transition: border-color 0.5s ease, box-shadow 0.5s ease, background 0.5s ease;">
            <!-- Orbs will be dynamically injected here via JS -->
        </div>
        
        <div id="orb-title-container" style="position: relative; width: 100%; height: 100px; margin-top: 20px; display: flex; justify-content: center; align-items: center;">
            <!-- Titles will cross-fade here -->
        </div>
        
        <button id="confirm-btn" onclick="document.getElementById('customize-modal').style.display='none';" style="margin-top: 30px; background: #111; border: 2px solid #ff00ff; color: #ff00ff; padding: 15px 50px; font-size: 24px; border-radius: 30px; cursor: pointer; text-transform: uppercase; font-weight: bold; box-shadow: 0 0 20px rgba(255,0,255,0.4); transition: border-color 0.5s ease, color 0.5s ease, box-shadow 0.5s ease;">CONFIRM</button>
    </div>

    <script>
    const orbs = [
        { id: 0, name: 'Default Neon', color: '#00ffff', src: 'none', titleSrc: null },
        { id: 1, name: 'Azure Core', color: '#0088ff', src: 'orb_1.png', titleSrc: 'title_1.png' },
        { id: 2, name: 'Crimson Eye', color: '#ff2222', src: 'orb_2.png', titleSrc: null },
        { id: 3, name: 'Emerald Reactor', color: '#22ff22', src: 'orb_3.png', titleSrc: 'title_3.png' },
        { id: 4, name: 'Amethyst Void', color: '#8822ff', src: 'orb_4.png', titleSrc: null },
        { id: 5, name: 'Solar Flare', color: '#ffff22', src: 'orb_5.png', titleSrc: 'title_5.png' },
        { id: 6, name: 'Molten Core', color: '#ff8822', src: 'orb_6.png', titleSrc: null },
        { id: 7, name: 'Cyan Pulse', color: '#22ffff', src: 'orb_7.png', titleSrc: 'title_7.png' },
        { id: 8, name: 'Magenta Spark', color: '#ff22ff', src: 'orb_8.png', titleSrc: null },
        { id: 9, name: 'Platinum Star', color: '#ffffff', src: 'orb_9.png', titleSrc: 'title_9.png' },
    ];

    function initCustomize() {
        const carousel = document.getElementById('orb-carousel');
        const titleContainer = document.getElementById('orb-title-container');
        const modalHeader = document.getElementById('modal-header');
        const confirmBtn = document.getElementById('confirm-btn');
        let selectedId = parseInt(localStorage.getItem('selectedOrbId') || '0', 10);
        
        // Pre-create title elements for cross-fading
        const titleElements = {};
        orbs.forEach(orb => {
            const wrapper = document.createElement('div');
            wrapper.style.cssText = 'position: absolute; display: flex; justify-content: center; align-items: center; width: 100%; height: 100%; transition: all 0.6s cubic-bezier(0.2, 0.8, 0.2, 1); opacity: 0; transform: translateY(10px) scale(0.95); pointer-events: none;';
            
            if (orb.titleSrc) {
                const img = document.createElement('img');
                img.src = orb.titleSrc;
                img.style.cssText = 'max-width: 100%; max-height: 100%; object-fit: contain; filter: drop-shadow(0 0 10px ' + orb.color + ');';
                wrapper.appendChild(img);
            } else {
                const txt = document.createElement('p');
                txt.textContent = orb.name;
                txt.style.cssText = 'color: ' + orb.color + '; font-size: 32px; font-weight: bold; text-transform: uppercase; text-shadow: 0 0 20px ' + orb.color + ', 0 0 40px ' + orb.color + '; letter-spacing: 2px;';
                wrapper.appendChild(txt);
            }
            
            titleContainer.appendChild(wrapper);
            titleElements[orb.id] = wrapper;
        });

        function updateModalTheme(color) {
            // Update surroundings to match the font style/color!
            modalHeader.style.color = color;
            modalHeader.style.textShadow = '0 0 15px ' + color;
            
            carousel.style.borderColor = color;
            carousel.style.boxShadow = '0 0 40px ' + color + '40'; // 40 is alpha in hex approx 25%
            carousel.style.background = 'radial-gradient(circle, ' + color + '10 0%, transparent 80%)';
            
            confirmBtn.style.borderColor = color;
            confirmBtn.style.color = color;
            confirmBtn.style.boxShadow = '0 0 20px ' + color + '60';
        }

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
            item.appendChild(visual);
            
            // Initialization for selected
            if (orb.id === selectedId) {
                item.style.background = 'rgba(255,255,255,0.15)';
                item.style.transform = 'scale(1.15)';
                item.style.boxShadow = '0 0 20px ' + orb.color;
                
                titleElements[orb.id].style.opacity = '1';
                titleElements[orb.id].style.transform = 'translateY(0) scale(1)';
                updateModalTheme(orb.color);
            }
            
            item.onclick = () => {
                localStorage.setItem('selectedOrbId', orb.id);
                localStorage.setItem('selectedOrbColor', orb.color);
                
                // Transition titles
                titleElements[selectedId].style.opacity = '0';
                titleElements[selectedId].style.transform = 'translateY(-10px) scale(0.95)';
                
                selectedId = orb.id;
                
                titleElements[selectedId].style.opacity = '1';
                titleElements[selectedId].style.transform = 'translateY(0) scale(1)';
                
                // visually update wheel items
                Array.from(carousel.children).forEach((child, idx) => {
                    const childColor = orbs[idx].color;
                    child.style.background = idx === selectedId ? 'rgba(255,255,255,0.15)' : 'transparent';
                    child.style.transform = idx === selectedId ? 'scale(1.15)' : 'scale(1)';
                    child.style.boxShadow = idx === selectedId ? '0 0 20px ' + childColor : 'none';
                });
                
                updateModalTheme(orb.color);
                
                item.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
                
                if (window.updateOrbSelection) {
                    window.updateOrbSelection(orb.id, orb.color, orb.src);
                }
            };
            
            carousel.appendChild(item);
        });
    }
    setTimeout(initCustomize, 100);
    </script>
</body>"""

html = re.sub(pattern, new_modal_block, html, flags=re.DOTALL)
with open('game.html', 'w') as f:
    f.write(html)
print("Updated game.html with cool transitions!")
