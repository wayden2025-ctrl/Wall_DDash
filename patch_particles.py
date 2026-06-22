import re

with open('game.js', 'r') as f:
    js = f.read()

# 1. Add getVaryingColor function near the top (e.g. after let selectedOrbColor)
vary_func = """
function getVaryingColor(hex) {
    if (!hex || hex.length !== 7) return hex;
    let r = parseInt(hex.slice(1,3), 16);
    let g = parseInt(hex.slice(3,5), 16);
    let b = parseInt(hex.slice(5,7), 16);
    
    const vary = () => Math.floor(Math.random() * 100 - 50); // +/- 50 variance for noticeable differences
    r = Math.min(255, Math.max(0, r + vary()));
    g = Math.min(255, Math.max(0, g + vary()));
    b = Math.min(255, Math.max(0, b + vary()));
    
    return `rgba(${r}, ${g}, ${b}, 0.8)`;
}
"""
js = js.replace('let selectedOrbColor = localStorage.getItem(\'selectedOrbColor\') || \'#00ffff\';', 'let selectedOrbColor = localStorage.getItem(\'selectedOrbColor\') || \'#00ffff\';\n' + vary_func)

# 2. Add particle spawning in update()
particle_spawn = """    // Player trail particles
    if (isPlaying) {
        for (let i = 0; i < 2; i++) {
            particles.push({
                size: 2 + Math.random() * 4,
                x: player.visualX + (Math.random() - 0.5) * PLAYER_RADIUS * 1.5,
                y: player.visualY + (Math.random() - 0.5) * PLAYER_RADIUS * 1.5,
                vx: (Math.random() - 0.5) * 60,
                vy: -Math.random() * 300 - 150, // Fly backwards fast
                color: getVaryingColor(selectedOrbColor),
                life: 0.4 + Math.random() * 0.4
            });
        }
    }

    // Spawning"""

js = js.replace('    // Spawning', particle_spawn)

with open('game.js', 'w') as f:
    f.write(js)
print("Added particle emission logic!")
