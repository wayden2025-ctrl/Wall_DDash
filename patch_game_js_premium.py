import re

with open('game.js', 'r') as f:
    js = f.read()

old_trail = r"""    // Player trail particles
    if \(isPlaying\) {
        for \(let i = 0; i < 2; i\+\+\) {
            particles\.push\({
                size: 2 \+ Math\.random\(\) \* 4,
                x: player\.visualX \+ \(Math\.random\(\) - 0\.5\) \* PLAYER_RADIUS \* 1\.5,
                y: player\.visualY \+ \(Math\.random\(\) - 0\.5\) \* PLAYER_RADIUS \* 1\.5,
                vx: \(Math\.random\(\) - 0\.5\) \* 60,
                vy: Math\.random\(\) \* 300 \+ 150, // Fly DOWNWARDS behind the player
                color: getVaryingColor\(selectedOrbColor\),
                life: 0\.15 \+ Math\.random\(\) \* 0\.2
            }\);
        }
    }"""

new_trail = """    // Player trail particles
    if (isPlaying) {
        const isPremium = selectedOrbId >= 10;
        const spawnCount = isPremium ? 5 : 2; 
        for (let i = 0; i < spawnCount; i++) {
            let pColor = getVaryingColor(selectedOrbColor);
            if (isPremium && Math.random() > 0.6) pColor = '#ffffff'; // Extra bright core sparks
            
            particles.push({
                size: (isPremium ? 3 : 2) + Math.random() * (isPremium ? 6 : 4),
                x: player.visualX + (Math.random() - 0.5) * PLAYER_RADIUS * (isPremium ? 2.5 : 1.5),
                y: player.visualY + (Math.random() - 0.5) * PLAYER_RADIUS * (isPremium ? 2.5 : 1.5),
                vx: (Math.random() - 0.5) * (isPremium ? 150 : 60),
                vy: Math.random() * (isPremium ? 500 : 300) + (isPremium ? 250 : 150),
                color: pColor,
                life: (isPremium ? 0.25 : 0.15) + Math.random() * 0.2
            });
        }
    }"""

js = re.sub(old_trail, new_trail, js)

with open('game.js', 'w') as f:
    f.write(js)
print("game.js patched.")
