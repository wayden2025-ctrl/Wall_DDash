import re

with open('game.js', 'r') as f:
    code = f.read()

# 1. Load the image
img_pattern = r"const spikeVariants = \["
img_replacement = """const droneImg = new Image();
droneImg.src = 'drone.png';

const spikeVariants = ["""
code = re.sub(img_pattern, img_replacement, code)

# 2. Adjust Bullet Spawn Y and Color
bullet_spawn_pattern = r"bullets\.push\(\{\s*x: drone\.x,\s*y: drone\.y,\s*vx: -600, // Left\s*radius: 6,\s*color: '#ff0055'\s*\}\);\s*bullets\.push\(\{\s*x: drone\.x,\s*y: drone\.y,\s*vx: 600, // Right\s*radius: 6,\s*color: '#ff0055'\s*\}\);"
bullet_spawn_replacement = """// Spawn bullets slightly above the drone's center to align with the side turrets
            bullets.push({
                x: drone.x - 20, // offset left
                y: drone.y - 5, // offset up
                vx: -600, // Left
                radius: 6,
                color: '#ff00ff' // Neon Pink
            });
            bullets.push({
                x: drone.x + 20, // offset right
                y: drone.y - 5, // offset up
                vx: 600, // Right
                radius: 6,
                color: '#ff00ff' // Neon Pink
            });"""
code = re.sub(bullet_spawn_pattern, bullet_spawn_replacement, code)

# 3. Draw Drone Image
draw_drone_pattern = r"// ── Drones ──.*?// Inner glowing eye.*?ctx\.fill\(\);\s*\}\);"
draw_drone_replacement = """// ── Drones ──
    drones.forEach(drone => {
        // Draw the drone image centered
        // Drone image is 119x119. Let's draw it at width 80, height 80.
        const dWidth = 80;
        const dHeight = 80;
        ctx.drawImage(droneImg, drone.x - dWidth / 2, drone.y - dHeight / 2, dWidth, dHeight);
    });"""
code = re.sub(draw_drone_pattern, draw_drone_replacement, code, flags=re.DOTALL)

with open('game.js', 'w') as f:
    f.write(code)

print("Drone image implementation applied.")
