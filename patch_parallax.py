import re

with open('game.js', 'r') as f:
    code = f.read()

# Fix loop() bgObjects update
loop_pattern = r"// Update parallax bg objects\s*bgObjects\.forEach\(bg => \{\s*bg\.y \+= currentSpeed \* dt \* bg\.speed \* 0\.001;\s*if \(bg\.y > 1\.2\) \{\s*bg\.y = -0\.2;\s*bg\.x = Math\.random\(\);\s*\}\s*\}\);"
loop_replacement = """// Update parallax bg objects (Smooth infinite scrolling)
    bgObjects.forEach(bg => {
        bg.y += currentSpeed * dt * bg.speed * 0.001;
        // If it goes fully below the screen
        if (bg.y * canvas.height > canvas.height + bg.height + 50) {
            bg.y = -(bg.height + 50) / canvas.height; // Teleport just above the screen
            bg.x = Math.random(); // Randomize horizontal position
            
            // Generate a fresh shape for variety!
            if (bg.layer === 2) {
                bg.width = 100 + Math.random() * 200;
                bg.height = 300 + Math.random() * 500;
                bg.type = Math.random() > 0.5 ? 'pillar' : 'frame';
            } else {
                bg.width = 30 + Math.random() * 80;
                bg.height = 100 + Math.random() * 200;
                bg.type = Math.random() > 0.3 ? 'frame' : 'lightstrip';
            }
        }
    });"""

code = re.sub(loop_pattern, loop_replacement, code)

# Fix draw() bgObjects calculation
draw_pattern = r"// ── Background Architecture Layers ──\s*bgObjects\.forEach\(bg => \{\s*// Calculate parallax Y using currentSpeed\s*let py = \(bg\.y \* h \+ \(scrollOffset \* bg\.speed\)\) % \(h \+ bg\.height\) - bg\.height;\s*let px = bg\.x \* w;"
draw_replacement = """// ── Background Architecture Layers ──
    bgObjects.forEach(bg => {
        let py = bg.y * h;
        let px = bg.x * w;"""

code = re.sub(draw_pattern, draw_replacement, code)

with open('game.js', 'w') as f:
    f.write(code)

print("Parallax optimized.")
