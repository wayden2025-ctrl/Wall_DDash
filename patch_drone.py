import re

with open('game.js', 'r') as f:
    code = f.read()

# 1. State arrays
state_pattern = r"let obstacles = \[\];\s*let particles = \[\];"
state_replacement = """let obstacles = [];
let drones = [];
let bullets = [];
let particles = [];"""
code = re.sub(state_pattern, state_replacement, code)

# 2. Reset logic
reset_pattern = r"obstacles = \[\];\s*particles = \[\];\s*ambientParticles = \[\];"
reset_replacement = """obstacles = [];
    drones = [];
    bullets = [];
    particles = [];
    ambientParticles = [];"""
code = re.sub(reset_pattern, reset_replacement, code)

# 3. Slow down player transition
lerp_pattern = r"const lerp = Math\.min\(1, 35 \* dt\); // faster horizontal snap"
lerp_replacement = r"const lerp = Math.min(1, 10 * dt); // slower dash for bullet dodging"
code = re.sub(lerp_pattern, lerp_replacement, code)

# 4. Spike Collision logic (remove lane check)
spike_col_pattern = r"// Collision\s*if \(ob\.lane === player\.lane && playerHitsSpike\(ob\)\) \{\s*gameOver\(\);\s*\}"
spike_col_replacement = """// Collision (uses raw geometry, no lane check needed)
        if (playerHitsSpike(ob)) {
            gameOver();
        }"""
code = re.sub(spike_col_pattern, spike_col_replacement, code)

# 5. Spawn logic
spawn_pattern = r"obstacles\.push\(\{\s*lane,\s*y: yPos,\s*height: spikeHeight,\s*depth: spikeDepth,\s*variant: variant,\s*passed: false\s*\}\);"
spawn_replacement = """// 20% chance to spawn a hacking drone INSTEAD of a spike
    if (Math.random() < 0.2 && combo > 10) { // Don't spawn drone instantly
        drones.push({
            x: canvas.width / 2,
            y: yPos,
            radius: 20,
            shootCooldown: 0.5 + Math.random() * 0.5,
            passed: false
        });
        // Still use the spike's dimensions for distance calculations
    } else {
        obstacles.push({
            lane,
            y: yPos,
            height: spikeHeight,
            depth: spikeDepth,
            variant: variant,
            passed: false
        });
    }"""
code = re.sub(spawn_pattern, spawn_replacement, code)

# Fix dashTimeDistance in spawnObstacle
dash_time_pattern = r"let dashTimeDistance = currentSpeed \* 0\.18;"
dash_time_replacement = r"let dashTimeDistance = currentSpeed * 0.45; // increased due to slower dash"
code = re.sub(dash_time_pattern, dash_time_replacement, code)

# 6. Update logic for Drones & Bullets
update_obs_pattern = r"// Remove offscreen\s*if \(ob\.y > canvas\.height \+ 50\) obstacles\.splice\(i, 1\);\s*\}"
update_obs_replacement = """// Remove offscreen
        if (ob.y > canvas.height + 50) obstacles.splice(i, 1);
    }

    // Update drones
    for (let i = drones.length - 1; i >= 0; i--) {
        const drone = drones[i];
        drone.y += currentSpeed * dt;
        
        if (!drone.passed && drone.y > player.y + PLAYER_RADIUS) {
            drone.passed = true;
            combo++;
            if (combo > maxCombo) maxCombo = combo;
        }

        // Shooting
        drone.shootCooldown -= dt;
        if (drone.shootCooldown <= 0) {
            // Shoot horizontally towards BOTH walls
            bullets.push({
                x: drone.x,
                y: drone.y,
                vx: -600, // Left
                radius: 6,
                color: '#ff0055'
            });
            bullets.push({
                x: drone.x,
                y: drone.y,
                vx: 600, // Right
                radius: 6,
                color: '#ff0055'
            });
            drone.shootCooldown = 1.0 + Math.random(); // wait before shooting again
            playTone(800, 0.05, 'sawtooth');
        }

        if (drone.y > canvas.height + 50) drones.splice(i, 1);
    }

    // Update bullets
    for (let i = bullets.length - 1; i >= 0; i--) {
        const b = bullets[i];
        b.x += b.vx * dt;
        
        // Check collision with player
        const dx = player.visualX - b.x;
        const dy = player.y - b.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < PLAYER_RADIUS + b.radius - 2) {
            gameOver();
        }

        // Remove if offscreen horizontally
        if (b.x < 0 || b.x > canvas.width) {
            bullets.splice(i, 1);
        }
    }"""
code = re.sub(update_obs_pattern, update_obs_replacement, code)

# 7. Draw logic
draw_obs_pattern = r"// ── Obstacles \(Spikes\) ──.*?ctx\.restore\(\);\s*\}"
draw_obs_replacement = """// ── Obstacles (Spikes) ──
    obstacles.forEach(ob => {
        ctx.save();
        if (ob.lane === 0) {
            ctx.translate(WALL_WIDTH, ob.y);
            ctx.scale(-1, 1);
            ctx.drawImage(ob.variant.img, -ob.depth, 0, ob.depth, ob.height);
        } else {
            ctx.translate(w - WALL_WIDTH - ob.depth, ob.y);
            ctx.drawImage(ob.variant.img, 0, 0, ob.depth, ob.height);
        }
        ctx.restore();
    });

    // ── Drones ──
    ctx.shadowBlur = 15;
    ctx.shadowColor = '#00ffff';
    drones.forEach(drone => {
        ctx.beginPath();
        ctx.arc(drone.x, drone.y, drone.radius, 0, Math.PI * 2);
        ctx.fillStyle = '#111';
        ctx.fill();
        ctx.lineWidth = 3;
        ctx.strokeStyle = '#00ffff';
        ctx.stroke();
        
        // Inner glowing eye
        ctx.beginPath();
        ctx.arc(drone.x, drone.y, drone.radius * 0.4, 0, Math.PI * 2);
        ctx.fillStyle = '#ff00ff';
        ctx.fill();
    });
    
    // ── Bullets ──
    ctx.shadowColor = '#ff0055';
    bullets.forEach(b => {
        ctx.beginPath();
        ctx.arc(b.x, b.y, b.radius, 0, Math.PI * 2);
        ctx.fillStyle = '#ffffff';
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = b.color;
        ctx.stroke();
        
        // Trail
        ctx.beginPath();
        ctx.moveTo(b.x, b.y);
        ctx.lineTo(b.x - (b.vx * 0.05), b.y);
        ctx.strokeStyle = b.color;
        ctx.lineWidth = b.radius * 2;
        ctx.stroke();
    });
    ctx.shadowBlur = 0;"""
code = re.sub(draw_obs_pattern, draw_obs_replacement, code, flags=re.DOTALL)

with open('game.js', 'w') as f:
    f.write(code)

print("Hacking Drone implemented.")
