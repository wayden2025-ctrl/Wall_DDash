import re

with open('game.js', 'r') as f:
    code = f.read()

draw_pattern = r"// ── Background Architecture Layers ──.*?// ── Layer 4: Atmospheric FX \(Drifting Particles\) ──"
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
    
    // ── Layer 4: Atmospheric FX (Drifting Particles) ──"""

new_code = re.sub(draw_pattern, matrix_draw, code, flags=re.DOTALL)
if new_code == code:
    print("FAILED TO MATCH!")
else:
    print("SUCCESS")
    with open('game.js', 'w') as f:
        f.write(new_code)
