import re

with open('game.js', 'r') as f:
    js = f.read()

# Add particle update logic right before updateUI() in update()
particle_update = """
    // Update active particles (trail, sparks, ambient)
    for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx * dt;
        p.y += p.vy * dt;
        if (p.life !== undefined) {
            p.life -= dt;
            if (p.life <= 0) particles.splice(i, 1);
        } else {
            // Fallback for particles without life (if any)
            if (p.y > canvas.height + 50 || p.y < -50 || p.x < -50 || p.x > canvas.width + 50) {
                particles.splice(i, 1);
            }
        }
    }

    updateUI();"""
js = js.replace('    updateUI();', particle_update)

# Add particle draw logic right after drawing the player/trail in draw()
particle_draw = """
    // ── Draw Particles ────────────────────────────
    particles.forEach(p => {
        ctx.fillStyle = p.color || '#00ffff';
        ctx.globalAlpha = p.life !== undefined ? Math.max(0, p.life) : 1;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
    });
    ctx.globalAlpha = 1.0;

    // ── Bottom Fog / Energy Mist ───────────────────────"""
js = js.replace('    // ── Bottom Fog / Energy Mist ───────────────────────', particle_draw)

with open('game.js', 'w') as f:
    f.write(js)
print("Patched particle simulation and rendering loops!")
