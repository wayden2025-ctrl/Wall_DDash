import re

with open('game.js', 'r') as f:
    js = f.read()

# 1. Add image loading
if 'const playerImage = new Image();' not in js:
    js = js.replace(
        "// UI Elements",
        "const playerImage = new Image();\nplayerImage.src = 'player.png';\n\n// UI Elements"
    )

# 2. Replace player drawing logic
old_draw = """        // Glow
        ctx.shadowBlur = 5;
        ctx.shadowColor = '#00ffff';
        ctx.fillStyle = '#00ffff';

        ctx.beginPath();
        ctx.arc(px, py, PLAYER_RADIUS, 0, Math.PI * 2);
        ctx.fill();

        // Inner bright core
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(px, py, PLAYER_RADIUS * 0.45, 0, Math.PI * 2);
        ctx.fill();

        ctx.shadowBlur = 0; // reset"""

new_draw = """        // Render Player Image
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
        
        ctx.shadowBlur = 0; // reset"""

if old_draw in js:
    js = js.replace(old_draw, new_draw)
    print("Player drawing replaced successfully.")
else:
    print("Could not find old draw block!")

with open('game.js', 'w') as f:
    f.write(js)
