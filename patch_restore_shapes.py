import re

with open('game.js', 'r') as f:
    code = f.read()

# 1. Restore bgObjects init
matrix_init_pattern = r"// ── Neon Hacker Matrix Rain Initialization ──.*?const NUM_STREAMS = 25;"
combined_init = """// ── Neon Hacker Matrix Rain Initialization ──
const matrixChars = "0179%#@&?!/\\[]{}<>XKRVNZ";
const matrixColors = ['#00ffff', '#ff00ff', '#8800ff', '#0088ff', '#ff00aa'];
let matrixStreams = [];
const NUM_STREAMS = 15; // Reduced matrix streams slightly to balance with shapes

for (let i = 0; i < NUM_STREAMS; i++) {
    matrixStreams.push(createMatrixStream(true));
}

// ── Background Architecture (Shapes & Lines) Initialization ──
let bgObjects = [];
// Distant Architecture (Layer 2)
for (let i = 0; i < 4; i++) { // Reduced count
    bgObjects.push({
        layer: 2,
        x: Math.random(),
        y: Math.random(),
        width: 100 + Math.random() * 200,
        height: 300 + Math.random() * 500,
        speed: 0.1 + Math.random() * 0.1,
        type: Math.random() > 0.5 ? 'pillar' : 'frame'
    });
}
// Midground Detail (Layer 3)
for (let i = 0; i < 8; i++) { // Reduced count
    bgObjects.push({
        layer: 3,
        x: Math.random(),
        y: Math.random(),
        width: 30 + Math.random() * 80,
        height: 100 + Math.random() * 200,
        speed: 0.2 + Math.random() * 0.2,
        type: Math.random() > 0.3 ? 'frame' : 'lightstrip'
    });
}"""

code = re.sub(matrix_init_pattern, combined_init, code, flags=re.DOTALL)

# 2. Restore bgObjects update
update_pattern = r"// Update Matrix Streams"
combined_update = """// Update Shapes
    bgObjects.forEach(bg => {
        bg.y += currentSpeed * dt * bg.speed * 0.001;
        if (bg.y * canvas.height > canvas.height + bg.height + 50) {
            bg.y = -(bg.height + 50) / canvas.height;
            bg.x = Math.random();
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
    });

    // Update Matrix Streams"""

code = re.sub(update_pattern, combined_update, code, flags=re.DOTALL)

# 3. Restore bgObjects draw
draw_pattern = r"// ── Matrix Code Rain ──"
combined_draw = """// ── Background Shapes ──
    bgObjects.forEach(bg => {
        let py = bg.y * h;
        let px = bg.x * w;

        ctx.beginPath();
        if (bg.layer === 2) {
            ctx.strokeStyle = 'rgba(100, 0, 150, 0.3)';
            ctx.fillStyle = 'rgba(20, 0, 40, 0.4)';
            ctx.lineWidth = 4;
            if (bg.type === 'pillar') {
                ctx.fillRect(px, py, bg.width, bg.height);
                ctx.strokeRect(px, py, bg.width, bg.height);
            } else if (bg.type === 'frame') {
                ctx.strokeRect(px, py, bg.width, bg.height);
                ctx.strokeRect(px + 15, py + 15, bg.width - 30, bg.height - 30);
            }
        } else if (bg.layer === 3) {
            ctx.strokeStyle = 'rgba(255, 0, 255, 0.4)';
            ctx.lineWidth = 2;
            if (bg.type === 'frame') {
                ctx.strokeRect(px, py, bg.width, bg.height);
                ctx.fillStyle = 'rgba(255, 0, 255, 0.05)';
                ctx.fillRect(px, py, bg.width, bg.height);
            } else if (bg.type === 'lightstrip') {
                ctx.strokeStyle = 'rgba(0, 255, 255, 0.5)';
                ctx.moveTo(px, py);
                ctx.lineTo(px, py + bg.height);
                ctx.stroke();
            }
        }
    });

    // ── Matrix Code Rain ──"""

code = re.sub(draw_pattern, combined_draw, code, flags=re.DOTALL)

with open('game.js', 'w') as f:
    f.write(code)

print("Shapes restored successfully.")
