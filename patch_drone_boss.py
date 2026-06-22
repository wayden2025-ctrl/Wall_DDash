import re

with open('game.js', 'r') as f:
    code = f.read()

# 1. Update Spawn Logic
spawn_pattern = r"// 20% chance to spawn a hacking drone INSTEAD of a spike.*?\} else \{"
spawn_replacement = """// Spawn drone if none active (Mini-boss phase)
    if (drones.length === 0 && Math.random() < 0.15 && combo > 10) { 
        drones.push({
            x: canvas.width / 2,
            y: yPos,
            state: 'entering',
            hoverTimer: 20.0, // Boss phase duration
            shootCooldown: 1.0 // Initial delay
        });
        // Still use the spike's dimensions for distance calculations
    } else {"""
code = re.sub(spawn_pattern, spawn_replacement, code, flags=re.DOTALL)

# 2. Update Drone Logic
drone_update_pattern = r"// Update drones\s*for \(let i = drones\.length - 1; i >= 0; i--\) \{.*?if \(drone\.y > canvas\.height \+ 50\) drones\.splice\(i, 1\);\s*\}"
drone_update_replacement = """// Update drones (Mini-Boss State Machine)
    for (let i = drones.length - 1; i >= 0; i--) {
        const drone = drones[i];
        
        if (drone.state === 'entering') {
            drone.y += currentSpeed * dt;
            if (drone.y >= 80) {
                drone.y = 80;
                drone.state = 'hovering';
            }
        } else if (drone.state === 'hovering') {
            drone.hoverTimer -= dt;
            if (drone.hoverTimer <= 0) {
                drone.state = 'leaving';
            }
            
            // Shooting vertically downwards from bottom cannon
            drone.shootCooldown -= dt;
            if (drone.shootCooldown <= 0) {
                bullets.push({
                    x: drone.x,
                    y: drone.y + 35, // Bottom cannon offset
                    vx: 0, 
                    vy: 700 + currentSpeed * 0.4, // Travels down fast
                    radius: 8,
                    color: '#ff00ff'
                });
                drone.shootCooldown = 0.4 + Math.random() * 0.2; // Rhythmic pulses
                playTone(800, 0.05, 'sawtooth');
            }
        } else if (drone.state === 'leaving') {
            // Fly upwards
            drone.y -= currentSpeed * dt * 1.5;
            if (drone.y < -150) {
                drones.splice(i, 1);
                continue;
            }
        }
    }"""
code = re.sub(drone_update_pattern, drone_update_replacement, code, flags=re.DOTALL)

# 3. Update Bullet Logic
bullet_update_pattern = r"// Update bullets\s*for \(let i = bullets\.length - 1; i >= 0; i--\) \{.*?if \(b\.x < 0 \|\| b\.x > canvas\.width\) \{\s*bullets\.splice\(i, 1\);\s*\}\s*\}"
bullet_update_replacement = """// Update bullets
    for (let i = bullets.length - 1; i >= 0; i--) {
        const b = bullets[i];
        b.x += (b.vx || 0) * dt;
        b.y += (b.vy || 0) * dt;
        
        // Check collision with player
        const dx = player.visualX - b.x;
        const dy = player.y - b.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < PLAYER_RADIUS + b.radius - 2) {
            gameOver();
        }

        // Remove if offscreen bottom
        if (b.y > canvas.height + 50) {
            bullets.splice(i, 1);
        }
    }"""
code = re.sub(bullet_update_pattern, bullet_update_replacement, code, flags=re.DOTALL)

# 4. Update Bullet Render (Trail)
bullet_trail_pattern = r"// Trail\s*ctx\.beginPath\(\);\s*ctx\.moveTo\(b\.x, b\.y\);\s*ctx\.lineTo\(b\.x - \(b\.vx \* 0\.05\), b\.y\);"
bullet_trail_replacement = """// Trail
        ctx.beginPath();
        ctx.moveTo(b.x, b.y);
        ctx.lineTo(b.x - ((b.vx || 0) * 0.05), b.y - ((b.vy || 0) * 0.05));"""
code = re.sub(bullet_trail_pattern, bullet_trail_replacement, code, flags=re.DOTALL)

with open('game.js', 'w') as f:
    f.write(code)

print("Drone mini-boss logic applied.")
