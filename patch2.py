import re

with open('game.js', 'r') as f:
    code = f.read()

draw_new = """function draw() {
    const w = canvas.width;
    const h = canvas.height;

    ctx.save();
    
    // Apply camera shake
    if (screenShakeTime > 0) {
        const shakeX = (Math.random() - 0.5) * screenShakeIntensity;
        const shakeY = (Math.random() - 0.5) * screenShakeIntensity;
        ctx.translate(shakeX, shakeY);
    }

    // ── Layer 1: Background (Deep Cyber Void) ──
    const bgGrad = ctx.createLinearGradient(0, 0, 0, h);
    bgGrad.addColorStop(0, '#0b001a'); // deep dark violet top
    bgGrad.addColorStop(1, '#1a0033'); // slightly brighter magenta-purple bottom
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, w, h);

    // ── Background Architecture Layers ──
    bgObjects.forEach(bg => {
        // Calculate parallax Y using currentSpeed
        let py = (bg.y * h + (scrollOffset * bg.speed)) % (h + bg.height) - bg.height;
        let px = bg.x * w;

        ctx.beginPath();
        if (bg.layer === 2) {
            // Distant Architecture
            ctx.shadowBlur = 10;
            ctx.shadowColor = '#440088';
            ctx.strokeStyle = 'rgba(100, 0, 150, 0.3)';
            ctx.fillStyle = 'rgba(20, 0, 40, 0.4)';
            ctx.lineWidth = 4;
            
            if (bg.type === 'pillar') {
                ctx.fillRect(px, py, bg.width, bg.height);
                ctx.strokeRect(px, py, bg.width, bg.height);
            } else if (bg.type === 'frame') {
                ctx.strokeRect(px, py, bg.width, bg.height);
                // Inner square
                ctx.strokeRect(px + 15, py + 15, bg.width - 30, bg.height - 30);
            }
        } else if (bg.layer === 3) {
            // Midground Detail
            ctx.shadowBlur = 15;
            ctx.shadowColor = '#ff00ff';
            ctx.strokeStyle = 'rgba(255, 0, 255, 0.4)';
            ctx.lineWidth = 2;
            
            if (bg.type === 'frame') {
                ctx.strokeRect(px, py, bg.width, bg.height);
                ctx.fillStyle = 'rgba(255, 0, 255, 0.05)';
                ctx.fillRect(px, py, bg.width, bg.height);
            } else if (bg.type === 'lightstrip') {
                ctx.shadowColor = '#00ffff';
                ctx.strokeStyle = 'rgba(0, 255, 255, 0.5)';
                ctx.moveTo(px, py);
                ctx.lineTo(px, py + bg.height);
                ctx.stroke();
            }
        }
        ctx.shadowBlur = 0;
    });

    // ── Layer 4: Atmospheric FX (Drifting Particles) ──
    ambientParticles.forEach(p => {
        let py = p.y * h;
        let px = p.x * w;
        ctx.shadowBlur = 10;
        ctx.shadowColor = p.color;
        ctx.fillStyle = p.color;
        ctx.globalAlpha = 0.6;
        ctx.beginPath();
        ctx.arc(px, py, p.size, 0, Math.PI * 2);
        ctx.fill();
    });
    ctx.globalAlpha = 1.0;
    ctx.shadowBlur = 0;

    // ── Draw Energy Tower Walls ───────────────────────
    const wallColor = '#120024'; // dark purple solid body
    ctx.fillStyle = wallColor; 
    
    // Left Wall Body
    ctx.fillRect(0, 0, WALL_WIDTH, h);
    // Right Wall Body
    ctx.fillRect(w - WALL_WIDTH, 0, WALL_WIDTH, h);

    // Wall texture/paneling (subtle grid/lines)
    ctx.strokeStyle = 'rgba(80, 0, 150, 0.2)';
    ctx.lineWidth = 1;
    for (let i = 0; i < h; i += 40) {
        let yShift = (i + scrollOffset) % h;
        ctx.strokeRect(0, yShift, WALL_WIDTH, 20);
        ctx.strokeRect(w - WALL_WIDTH, yShift, WALL_WIDTH, 20);
    }

    // Glowing inner edge trim (Hot Pink / Magenta)
    ctx.shadowBlur = 25;
    ctx.shadowColor = '#ff00aa';
    ctx.strokeStyle = '#ff00aa';
    ctx.lineWidth = 4;

    ctx.beginPath();
    ctx.moveTo(WALL_WIDTH, 0);
    ctx.lineTo(WALL_WIDTH, h);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(w - WALL_WIDTH, 0);
    ctx.lineTo(w - WALL_WIDTH, h);
    ctx.stroke();
    
    // Add white hot edge highlight
    ctx.shadowBlur = 5;
    ctx.shadowColor = '#ffffff';
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(WALL_WIDTH, 0);
    ctx.lineTo(WALL_WIDTH, h);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(w - WALL_WIDTH, 0);
    ctx.lineTo(w - WALL_WIDTH, h);
    ctx.stroke();
    ctx.shadowBlur = 0;

    // ── Draw Multi-layered Crystal Obstacles ────────
    obstacles.forEach(ob => {
        if (ob.passed) {
            ctx.globalAlpha = Math.max(0, 1 - (ob.y - player.y) / 300);
        }
        
        ctx.save();
        
        // Add strong bloom to spikes
        ctx.shadowBlur = 20;
        ctx.shadowColor = '#ff00ff';
        
        if (ob.lane === 0) {
            // Left wall
            ctx.translate(WALL_WIDTH, ob.y);
            // Flip so the base is on the left
            ctx.scale(-1, 1);
            ctx.drawImage(ob.variant.img, -ob.depth, 0, ob.depth, ob.height);
        } else {
            // Right wall
            ctx.translate(w - WALL_WIDTH - ob.depth, ob.y);
            ctx.drawImage(ob.variant.img, 0, 0, ob.depth, ob.height);
        }
        ctx.restore();
        ctx.globalAlpha = 1;
    });

    // ── Draw Player Energy Core ───────────────────────
    ctx.shadowBlur = 25;
    ctx.shadowColor = '#00ffff'; // Electric cyan glow
    ctx.fillStyle = '#ffffff'; // White hot center
    
    ctx.beginPath();
    // Make the player look like a faceted crystal core (diamond shape)
    ctx.moveTo(player.visualX, player.y - PLAYER_RADIUS * 1.5); // Top
    ctx.lineTo(player.visualX + PLAYER_RADIUS * 1.2, player.y); // Right
    ctx.lineTo(player.visualX, player.y + PLAYER_RADIUS * 1.5); // Bottom
    ctx.lineTo(player.visualX - PLAYER_RADIUS * 1.2, player.y); // Left
    ctx.closePath();
    ctx.fill();

    // Inner core
    ctx.shadowBlur = 0;
    ctx.fillStyle = '#ccffff';
    ctx.beginPath();
    ctx.moveTo(player.visualX, player.y - PLAYER_RADIUS * 0.8);
    ctx.lineTo(player.visualX + PLAYER_RADIUS * 0.6, player.y);
    ctx.lineTo(player.visualX, player.y + PLAYER_RADIUS * 0.8);
    ctx.lineTo(player.visualX - PLAYER_RADIUS * 0.6, player.y);
    ctx.closePath();
    ctx.fill();

    // ── Particles ─────────────────────────────────────
    particles.forEach(p => {
        ctx.globalAlpha = p.life;
        ctx.fillStyle = p.color;
        ctx.shadowBlur = 10;
        ctx.shadowColor = p.color;
        
        ctx.beginPath();
        // Tiny glowing squares for cyber feel
        ctx.rect(p.x - p.size, p.y - p.size, p.size*2, p.size*2);
        ctx.fill();
    });
    ctx.globalAlpha = 1;
    ctx.shadowBlur = 0;
    
    // ── Bottom Fog / Energy Mist ───────────────────────
    const fogGrad = ctx.createLinearGradient(0, h - 150, 0, h);
    fogGrad.addColorStop(0, 'rgba(255, 0, 255, 0)');
    fogGrad.addColorStop(1, 'rgba(200, 0, 255, 0.4)');
    ctx.fillStyle = fogGrad;
    ctx.fillRect(0, h - 150, w, 150);

    // ── HUD ───────────────────────────────────────────
    drawHUD(w, h);

    ctx.restore();
}

"""

pattern = re.compile(r"function draw\(\) \{.*?(?=\n// ════════════════════════════════════════════════════════════════\n//  SCI-FI HUD)", re.DOTALL)
new_code = pattern.sub(draw_new, code)

if new_code == code:
    print("FAILED TO MATCH DRAW FUNCTION!")
else:
    print("SUCCESSFULLY MATCHED AND REPLACED DRAW FUNCTION")

with open('game.js', 'w') as f:
    f.write(new_code)
