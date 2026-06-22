import re

with open('game.js', 'r') as f:
    code = f.read()

# 1. Optimize background layer shadowBlur (remove it)
code = re.sub(r'ctx\.shadowBlur\s*=\s*10;\s*ctx\.shadowColor\s*=\s*\'#440088\';', '', code)
code = re.sub(r'ctx\.shadowBlur\s*=\s*15;\s*ctx\.shadowColor\s*=\s*\'#ff00ff\';', '', code)

# 2. Optimize ambientParticles shadowBlur
code = re.sub(r'ctx\.shadowBlur\s*=\s*10;\s*ctx\.shadowColor\s*=\s*p\.color;', '', code)

# 3. Optimize Wall trim shadowBlur by replacing it with a layered approach (or just simple line without blur)
wall_trim_pattern = r"// Glowing inner edge trim \(Hot Pink / Magenta\)\s*ctx\.shadowBlur\s*=\s*25;\s*ctx\.shadowColor\s*=\s*'#ff00aa';\s*ctx\.strokeStyle\s*=\s*'#ff00aa';\s*ctx\.lineWidth\s*=\s*4;"
wall_trim_replacement = """// Glowing inner edge trim (Hot Pink / Magenta)
    ctx.strokeStyle = '#ff00aa';
    ctx.lineWidth = 4;"""
code = re.sub(wall_trim_pattern, wall_trim_replacement, code)

# Remove white hot edge shadowBlur
code = re.sub(r"// Add white hot edge highlight\s*ctx\.shadowBlur\s*=\s*5;\s*ctx\.shadowColor\s*=\s*'#ffffff';", "// Add white hot edge highlight\n", code)

# 4. Remove spike bloom
code = re.sub(r"// Add strong bloom to spikes\s*ctx\.shadowBlur\s*=\s*20;\s*ctx\.shadowColor\s*=\s*'#ff00ff';", "// Spike bloom removed for performance", code)

# 5. Remove 'particles' rendering block (the comet trail squares) entirely from draw()
particles_draw_pattern = r"// ── Particles ─────────────────────────────────────\s*particles\.forEach.*?ctx\.shadowBlur\s*=\s*0;"
code = re.sub(particles_draw_pattern, "", code, flags=re.DOTALL)

# 6. Remove particles from loop() and spawnObstacle (if any extra was added)
code = re.sub(r"// Heavy player comet trail\s*if \(isPlaying\) \{.*?\n    \}\n\n", "", code, flags=re.DOTALL)

# 7. Replace the Player rendering
player_old_pattern = r"// ── Draw Player Energy Core ───────────────────────.*?ctx\.shadowBlur\s*=\s*0;"
player_new = """// ── Draw Player ───────────────────────────
    if (isPlaying || true) {
        const px = player.visualX;
        const py = player.visualY || player.y;

        // Glow (keep a small shadowBlur for the player since it's just one object)
        ctx.shadowBlur = 10;
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

        ctx.shadowBlur = 0;

        // Trail
        ctx.globalAlpha = 0.25;
        ctx.fillStyle = '#00ffff';
        ctx.beginPath();
        ctx.arc(px, py + 8, PLAYER_RADIUS * 0.7, 0, Math.PI * 2);
        ctx.fill();
        ctx.arc(px, py + 16, PLAYER_RADIUS * 0.4, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
    }"""
code = re.sub(player_old_pattern, player_new, code, flags=re.DOTALL)

# Ensure trailing ctx.shadowBlur = 0; is cleared at end of bgObjects
code = code.replace("ctx.shadowBlur = 0;", "")
code = code.replace("ctx.shadowBlur = 10;", "")
code = code.replace("ctx.shadowBlur = p.isAmbient ? 4 : 10;", "")

# Re-add player shadow blur properly since we just removed all of them above
player_new_fixed = """// ── Draw Player ───────────────────────────
    if (isPlaying || true) {
        const px = player.visualX;
        const py = player.visualY || player.y;

        // Glow
        ctx.shadowBlur = 15;
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

        ctx.shadowBlur = 0; // reset

        // Trail
        ctx.globalAlpha = 0.25;
        ctx.fillStyle = '#00ffff';
        ctx.beginPath();
        ctx.arc(px, py + 8, PLAYER_RADIUS * 0.7, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(px, py + 16, PLAYER_RADIUS * 0.4, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
    }"""
code = re.sub(r"// ── Draw Player ───────────────────────────.*?ctx\.globalAlpha = 1;\n    \}", player_new_fixed, code, flags=re.DOTALL)

# HUD shadowBlur optimization
code = re.sub(r"ctx\.shadowBlur = 30;", "ctx.shadowBlur = 10;", code)
code = re.sub(r"ctx\.shadowBlur = 15;", "ctx.shadowBlur = 5;", code)

with open('game.js', 'w') as f:
    f.write(code)

print("Done optimizing.")
