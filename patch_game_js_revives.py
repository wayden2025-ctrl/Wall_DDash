import re

with open('game.js', 'r') as f:
    js = f.read()

# 1. Add initRevives and global variables
revive_globals = """
let revivesLeft = 3;
let isReviving = false;
let reviveTimer = 0;

function initRevives() {
    const today = new Date().toDateString();
    const lastReviveDate = localStorage.getItem('lastReviveDate');
    let savedRevives = parseInt(localStorage.getItem('revivesLeft'));
    if (isNaN(savedRevives)) savedRevives = 3;
    
    if (lastReviveDate !== today) {
        if (savedRevives < 3) savedRevives = 3;
        localStorage.setItem('lastReviveDate', today);
        localStorage.setItem('revivesLeft', savedRevives.toString());
    }
    
    revivesLeft = savedRevives;
}

function revivePlayer() {
    if (revivesLeft <= 0) return;
    
    revivesLeft--;
    localStorage.setItem('revivesLeft', revivesLeft.toString());
    
    gameOverScreen.classList.add('hidden');
    
    // Clear obstacles around the player
    for (let i = obstacles.length - 1; i >= 0; i--) {
        const obs = obstacles[i];
        if (Math.abs(obs.y - player.y) < 800) {
            obstacles.splice(i, 1);
        }
    }
    
    isReviving = true;
    reviveTimer = 3.2; // slight buffer
    
    lastTime = performance.now();
    requestAnimationFrame(reviveLoop);
}

function reviveLoop(timestamp) {
    if (!isReviving) return;
    
    let rawDt = (timestamp - lastTime) / 1000;
    if (rawDt > 0.1) rawDt = 0.1;
    lastTime = timestamp;
    
    reviveTimer -= rawDt;
    
    draw(); // Redraw game state
    
    // Draw countdown
    ctx.save();
    ctx.fillStyle = `rgba(0, 255, 255, 1)`;
    ctx.font = 'bold 150px Courier New';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.shadowBlur = 30;
    ctx.shadowColor = '#00ffff';
    const num = Math.ceil(reviveTimer);
    if (num > 0) {
        // pulse effect
        const scale = 1 + (num - reviveTimer);
        ctx.translate(canvas.width/2, canvas.height/2);
        ctx.scale(scale, scale);
        ctx.fillText(num, 0, 0);
    }
    ctx.restore();
    
    if (reviveTimer <= 0) {
        isReviving = false;
        isPlaying = true;
        lastTime = performance.now();
        requestAnimationFrame(loop);
    } else {
        requestAnimationFrame(reviveLoop);
    }
}
"""

# Inject after global variables
js = js.replace("let maxCombo = parseInt(localStorage.getItem('maxCombo')) || 0;", "let maxCombo = parseInt(localStorage.getItem('maxCombo')) || 0;\n" + revive_globals)

# 2. Call initRevives() at the end
js = js.replace("initCustomize();", "initCustomize();\ninitRevives();")

# 3. Update gameOver() to configure the revive button
old_game_over = """function gameOver() {
    isPlaying = false;
    playHit();
    container.classList.add('shake');
    setTimeout(() => container.classList.remove('shake'), 300);
    spawnParticles(player.visualX, player.y, '#00ffff');

    gameOverScreen.classList.remove('hidden');
    finalScoreEl.innerText = Math.floor(score);
    finalComboEl.innerText = maxCombo;
}"""

new_game_over = """function gameOver() {
    isPlaying = false;
    playHit();
    container.classList.add('shake');
    setTimeout(() => container.classList.remove('shake'), 300);
    spawnParticles(player.visualX, player.y, '#00ffff');

    gameOverScreen.classList.remove('hidden');
    finalScoreEl.innerText = Math.floor(score);
    finalComboEl.innerText = maxCombo;
    
    const reviveBtn = document.getElementById('revive-btn');
    if (reviveBtn) {
        if (revivesLeft > 0) {
            reviveBtn.innerHTML = `REVIVE (${revivesLeft} Left)`;
            reviveBtn.onclick = revivePlayer;
            reviveBtn.style.background = 'linear-gradient(45deg, #00ffaa, #0088ff)';
            reviveBtn.style.boxShadow = '0 0 20px rgba(0,255,170,0.6)';
        } else {
            reviveBtn.innerHTML = 'BUY MORE REVIVES';
            reviveBtn.onclick = () => window.location.href = 'https://buy.stripe.com/test_revives';
            reviveBtn.style.background = 'linear-gradient(45deg, #ffaa00, #ff0055)';
            reviveBtn.style.boxShadow = '0 0 20px rgba(255,170,0,0.6)';
        }
    }
}"""

js = js.replace(old_game_over, new_game_over)

with open('game.js', 'w') as f:
    f.write(js)
print("game.js patched with revive logic.")
