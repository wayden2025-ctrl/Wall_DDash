import re

with open('game.js', 'r') as f:
    js = f.read()

# 1. Add player.history = [] to startGame()
js = js.replace(
    'obstacles = [];',
    'obstacles = [];\n    player.history = [];'
)

# 2. Update history in update() loop
js = js.replace(
    'player.visualY = player.y - arcHeight;',
    """player.visualY = player.y - arcHeight;
    player.history = player.history || [];
    player.history.push({x: player.visualX, y: player.visualY});
    if (player.history.length > 12) player.history.shift();"""
)

# 3. Increase shadow glow for orb rendering
js = js.replace(
    'ctx.shadowBlur = selectedOrbId === 0 ? 5 : 20;',
    'ctx.shadowBlur = selectedOrbId === 0 ? 15 : 45;'
)

# 4. Replace static trail with dynamic history trail
old_trail = """        // Trail
        ctx.globalAlpha = 0.25;
        ctx.fillStyle = selectedOrbColor;
        ctx.beginPath();
        ctx.arc(px, py + 8, PLAYER_RADIUS * 0.7, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(px, py + 16, PLAYER_RADIUS * 0.4, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1.0;"""

new_trail = """        // Dynamic Motion Trail
        if (player.history) {
            ctx.shadowBlur = 20;
            ctx.shadowColor = selectedOrbColor;
            for (let i = 0; i < player.history.length; i++) {
                const pt = player.history[i];
                const ratio = i / player.history.length;
                ctx.globalAlpha = ratio * 0.6; // Fades out towards the tail
                ctx.fillStyle = selectedOrbColor;
                ctx.beginPath();
                ctx.arc(pt.x, pt.y, PLAYER_RADIUS * (0.3 + 0.7 * ratio), 0, Math.PI * 2);
                ctx.fill();
            }
        }
        ctx.globalAlpha = 1.0;
        ctx.shadowBlur = 0;"""

js = js.replace(old_trail, new_trail)

with open('game.js', 'w') as f:
    f.write(js)
print("Added dynamic trails and enhanced glows!")
