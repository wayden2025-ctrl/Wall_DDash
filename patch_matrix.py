import re

with open('game.js', 'r') as f:
    code = f.read()

# 1. Initialization
init_pattern = r"// Initialize Neon Background Architectural Elements.*?window\.ambientParticles = \[\];"
matrix_init = """// ── Neon Hacker Matrix Rain Initialization ──
const matrixChars = "0179%#@&?!/\\[]{}<>XKRVNZ";
const matrixColors = ['#00ffff', '#ff00ff', '#8800ff', '#0088ff', '#ff00aa'];
let matrixStreams = [];
const NUM_STREAMS = 25; // Sparse enough to not lag, dense enough to look cool

for (let i = 0; i < NUM_STREAMS; i++) {
    matrixStreams.push(createMatrixStream(true));
}

function createMatrixStream(randomY = false) {
    const length = 5 + Math.floor(Math.random() * 15);
    const symbols = [];
    for (let j = 0; j < length; j++) {
        symbols.push(matrixChars[Math.floor(Math.random() * matrixChars.length)]);
    }
    
    return {
        x: Math.random(), // 0 to 1
        y: randomY ? Math.random() : -0.5, // 0 to 1 on screen, or off-screen top
        speed: 0.1 + Math.random() * 0.4,
        length: length,
        symbols: symbols,
        colorBase: matrixColors[Math.floor(Math.random() * matrixColors.length)],
        layer: Math.random() > 0.6 ? 1 : (Math.random() > 0.4 ? 2 : 3), // 1=Front, 2=Mid, 3=Back
        fontSize: 0, // Computed in draw
        glitchTimer: Math.random()
    };
}

window.ambientParticles = [];"""
code = re.sub(init_pattern, matrix_init, code, flags=re.DOTALL)

# 2. Update logic
update_pattern = r"// Update parallax bg objects \(Smooth infinite scrolling\)\s*bgObjects\.forEach\(bg => \{.*?\}\);"
matrix_update = """// Update Matrix Streams
    matrixStreams.forEach(stream => {
        stream.y += currentSpeed * dt * stream.speed * 0.001;
        
        // Glitch effect
        stream.glitchTimer -= dt;
        if (stream.glitchTimer <= 0) {
            stream.glitchTimer = 0.1 + Math.random() * 0.5;
            // Swap a random character
            const idx = Math.floor(Math.random() * stream.length);
            stream.symbols[idx] = matrixChars[Math.floor(Math.random() * matrixChars.length)];
        }

        // If head is completely off screen bottom (approximate length via fontSize assumption)
        const approxStreamHeight = (stream.length * 20) / canvas.height; 
        if (stream.y - approxStreamHeight > 1.0) {
            // Respawn
            Object.assign(stream, createMatrixStream(false));
        }
    });"""
code = re.sub(update_pattern, matrix_update, code, flags=re.DOTALL)

# 3. Draw logic
draw_pattern = r"// ── Background Architecture Layers ──.*?ctx\.shadowBlur = 0;\s*\n\s*\n\s*// ── Layer 4: Atmospheric FX"
matrix_draw = """// ── Matrix Code Rain ──
    ctx.font = 'bold 16px "Courier New", monospace';
    ctx.textAlign = 'center';
    
    matrixStreams.forEach(stream => {
        let px = stream.x * w;
        let py = stream.y * h;
        
        let sizeMultiplier = 1;
        let baseAlpha = 1;
        
        if (stream.layer === 1) { sizeMultiplier = 1.2; baseAlpha = 1.0; }
        else if (stream.layer === 2) { sizeMultiplier = 0.9; baseAlpha = 0.6; }
        else { sizeMultiplier = 0.6; baseAlpha = 0.3; }
        
        ctx.font = `bold ${Math.floor(16 * sizeMultiplier)}px "Courier New", monospace`;
        
        for (let i = 0; i < stream.length; i++) {
            let charY = py - (i * 16 * sizeMultiplier);
            if (charY < -20 || charY > h + 20) continue; // Culling
            
            ctx.globalAlpha = baseAlpha * (1 - (i / stream.length));
            
            if (i === 0) {
                // Head character
                ctx.fillStyle = '#ffffff'; 
            } else {
                // Body character
                ctx.fillStyle = stream.colorBase;
            }
            
            ctx.fillText(stream.symbols[i], px, charY);
        }
    });
    ctx.globalAlpha = 1.0;
    
    // ── Layer 4: Atmospheric FX"""
code = re.sub(draw_pattern, matrix_draw, code, flags=re.DOTALL)

# 4. Remove `let bgObjects = [];` if present
code = re.sub(r"let bgObjects = \[\];\s*\n", "", code)

with open('game.js', 'w') as f:
    f.write(code)

print("Matrix Code Rain applied.")
