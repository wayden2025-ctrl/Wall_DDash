import re

with open('game.js', 'r') as f:
    js = f.read()

# 1. Remove the old playerImage load
js = js.replace("const playerImage = new Image();\nplayerImage.src = 'player.png';", "")

# 2. Add Orb Customization logic at the top
orb_init = """// --- Orb Customization ---
let selectedOrbId = parseInt(localStorage.getItem('selectedOrbId') || '0', 10);
let selectedOrbColor = localStorage.getItem('selectedOrbColor') || '#00ffff';
let customOrbImage = null;

if (selectedOrbId > 0) {
    customOrbImage = new Image();
    customOrbImage.src = 'orb_' + selectedOrbId + '.png';
}
"""
if '// --- Orb Customization ---' not in js:
    js = js.replace("// UI Elements", orb_init + "\n// UI Elements")

# 3. Replace player drawing block
old_draw = """    // ── Draw Player ───────────────────────────
    if (isPlaying || true) {
        const px = player.visualX;
        const py = player.visualY || player.y;

        // Render Player Image
        // Scale image relative to hitbox radius. The image has a bit of built-in transparent padding.
        const playerSize = PLAYER_RADIUS * 2 * 1.8; 
        
        // Add short neon glow vibrance
        ctx.shadowBlur = 20; 
        ctx.shadowColor = '#00ffff';
        
        ctx.drawImage(
            playerImage,
            px - playerSize / 2,
            py - playerSize / 2,
            playerSize,
            playerSize
        );
        
        ctx.shadowBlur = 0; // reset

        // Trail
        ctx.globalAlpha = 0.25;
        ctx.fillStyle = '#00ffff';
        ctx.beginPath();
        ctx.arc(px, py + 8, PLAYER_RADIUS * 0.7, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.globalAlpha = 1;
    }"""

new_draw = """    // ── Draw Player ───────────────────────────
    if (isPlaying || true) {
        const px = player.visualX;
        const py = player.visualY || player.y;

        ctx.shadowBlur = selectedOrbId === 0 ? 5 : 20;
        ctx.shadowColor = selectedOrbColor;

        if (selectedOrbId === 0) {
            // Draw procedural default neon ring
            ctx.fillStyle = selectedOrbColor;
            ctx.beginPath();
            ctx.arc(px, py, PLAYER_RADIUS, 0, Math.PI * 2);
            ctx.fill();

            // Inner bright core
            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.arc(px, py, PLAYER_RADIUS * 0.45, 0, Math.PI * 2);
            ctx.fill();
        } else {
            // Draw custom orb
            const playerSize = PLAYER_RADIUS * 2 * 1.8; 
            if (customOrbImage && customOrbImage.complete) {
                ctx.drawImage(
                    customOrbImage,
                    px - playerSize / 2,
                    py - playerSize / 2,
                    playerSize,
                    playerSize
                );
            }
        }
        ctx.shadowBlur = 0; // reset

        // Trail
        ctx.globalAlpha = 0.25;
        ctx.fillStyle = selectedOrbColor;
        ctx.beginPath();
        ctx.arc(px, py + 8, PLAYER_RADIUS * 0.7, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.globalAlpha = 1;
    }"""

if old_draw in js:
    js = js.replace(old_draw, new_draw)
    print("Player draw logic replaced.")
else:
    print("Failed to find old draw logic.")

with open('game.js', 'w') as f:
    f.write(js)
