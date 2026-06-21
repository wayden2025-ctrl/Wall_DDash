const canvas = document.getElementById('game-canvas');
const ctx = canvas.getContext('2d');
const container = document.getElementById('game-container');

// UI Elements
const scoreDisplay = document.getElementById('score-display');
const comboDisplay = document.getElementById('combo-display');
const perfectText = document.getElementById('perfect-text');
const startScreen = document.getElementById('start-screen');
const gameOverScreen = document.getElementById('game-over-screen');
const startBtn = document.getElementById('start-btn');
const restartBtn = document.getElementById('restart-btn');
const finalScoreEl = document.getElementById('final-score');
const finalComboEl = document.getElementById('final-combo');
const winScreen = document.getElementById('win-screen');
const winScoreEl = document.getElementById('win-score');
const winComboEl = document.getElementById('win-combo');
const winTimeEl = document.getElementById('win-time');
const winRestartBtn = document.getElementById('win-restart-btn');

// ─── Layout Constants ──────────────────────────────────────────
const WALL_WIDTH = 6;          // thickness of each white wall
const SPIKE_BASE = 30;         // spike height along the wall (vertical size)
const SPIKE_DEPTH = 50;        // how far the spike juts inward
const PLAYER_RADIUS = 12;      // player is a small circle on the wall

// ─── Game State ────────────────────────────────────────────────
let isPlaying = false;
let score = 0;
let combo = 0;
let maxCombo = 0;
let timeSurvived = 0;
let baseSpeed = 400;           // start chill
let currentSpeed = 400;
let timeScale = 1;
let lastTime = 0;

// ─── Player ────────────────────────────────────────────────────
const player = {
    lane: 0,     // 0 = left wall, 1 = right wall
    y: 0,        // set on resize (near bottom)
    x: 0,        // computed from lane
    targetX: 0,
    visualX: 0   // smoothly interpolated for drawing
};

// ─── Obstacles & Particles ─────────────────────────────────────
let obstacles = [];
let particles = [];
let spawnTimer = 0;
const SPAWN_INTERVAL = 0.45;  // spawn every 0.45s – dense but playable
const MIN_SPIKE_GAP = 50;     // minimum vertical px between any two spikes on the same wall
let lastSpawnLane = -1;        // track last wall to alternate

// ─── Near-miss / perfect thresholds (vertical px) ──────────────
const NEAR_MISS_DIST = 90;
const PERFECT_DIST = 35;

// ─── Scrolling grid lines (cosmetic) ──────────────────────────
let scrollOffset = 0;

// ════════════════════════════════════════════════════════════════
//  RESIZE
// ════════════════════════════════════════════════════════════════
function resize() {
    canvas.width  = container.clientWidth;
    canvas.height = container.clientHeight;
    player.y = canvas.height - 120;
    setPlayerX(true);
}
window.addEventListener('resize', resize);

function setPlayerX(instant) {
    if (player.lane === 0) {
        player.targetX = WALL_WIDTH + PLAYER_RADIUS + 2;
    } else {
        player.targetX = canvas.width - WALL_WIDTH - PLAYER_RADIUS - 2;
    }
    if (instant) player.visualX = player.targetX;
}

// ════════════════════════════════════════════════════════════════
//  INPUT
// ════════════════════════════════════════════════════════════════
function switchLane() {
    if (!isPlaying) return;
    player.lane = player.lane === 0 ? 1 : 0;
    setPlayerX(false);
    playTone(300 + player.lane * 100, 0.05, 'triangle');
    checkNearMiss();
}

window.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
        e.preventDefault();
        if (!isPlaying && !startScreen.classList.contains('hidden')) startGame();
        else if (!isPlaying && !gameOverScreen.classList.contains('hidden')) restartGame();
        else switchLane();
    }
});

canvas.addEventListener('mousedown', (e) => {
    if (!isPlaying && !startScreen.classList.contains('hidden')) return;
    if (!isPlaying && !gameOverScreen.classList.contains('hidden')) return;
    switchLane();
});

canvas.addEventListener('touchstart', (e) => {
    if (e.target.tagName !== 'BUTTON') {
        e.preventDefault();
        if (!isPlaying && !startScreen.classList.contains('hidden')) return;
        if (!isPlaying && !gameOverScreen.classList.contains('hidden')) return;
        switchLane();
    }
}, { passive: false });

startBtn.addEventListener('click', startGame);
restartBtn.addEventListener('click', restartGame);
winRestartBtn.addEventListener('click', restartGame);

// ════════════════════════════════════════════════════════════════
//  AUDIO (synthesized – no external assets)
// ════════════════════════════════════════════════════════════════
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playTone(freq, duration, type = 'sine', volume = 0.1) {
    if (audioCtx.state === 'suspended') audioCtx.resume();
    const osc  = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
    gain.gain.setValueAtTime(volume, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + duration);
}

function playHit() {
    playTone(100, 0.2, 'sawtooth', 0.2);
    playTone(50, 0.3, 'square', 0.15);
}

function playNearMiss() {
    playTone(600, 0.1, 'sine', 0.08);
}

function playPerfect() {
    playTone(800, 0.1, 'sine', 0.1);
    setTimeout(() => playTone(1200, 0.15, 'sine', 0.1), 50);
}

// ════════════════════════════════════════════════════════════════
//  OBSTACLE SPAWNING
//  RULES:
//    • Never place spikes on both walls at the same Y level.
//    • Enforce a minimum vertical gap on the SAME wall so the
//      player always has time to react after switching.
// ════════════════════════════════════════════════════════════════
function canSpawnOnLane(lane, yPos) {
    for (const ob of obstacles) {
        // Same wall? enforce vertical gap (shrinks drastically in hell mode)
        const currentMinGap = score >= 950000 ? 25 : MIN_SPIKE_GAP;
        if (ob.lane === lane && Math.abs(ob.y - yPos) < currentMinGap) return false;
        // Opposite wall at same Y? never
        if (ob.lane !== lane && Math.abs(ob.y - yPos) < SPIKE_BASE + 4) return false;
    }
    return true;
}

function spawnObstacle() {
    const yPos = -SPIKE_BASE;
    // Alternate walls or add randomness based on phase
    let lane;
    if (lastSpawnLane === -1) {
        lane = Math.random() < 0.5 ? 0 : 1; 
    } else if (score >= 50000 && score < 950000) {
        // Mid-to-late: "more randomness", purely random 50/50 to spread everywhere
        lane = Math.random() < 0.5 ? 0 : 1;
    } else {
        // Early game and Hell mode: perfect alternate
        lane = lastSpawnLane === 0 ? 1 : 0;
    }

    if (!canSpawnOnLane(lane, yPos)) {
        lane = lane === 0 ? 1 : 0;
        if (!canSpawnOnLane(lane, yPos)) {
            spawnTimer = 0.08; // retry fast
            return;
        }
    }

    lastSpawnLane = lane;

    obstacles.push({
        lane,
        y: yPos,
        height: SPIKE_BASE + Math.random() * 60,
        depth: SPIKE_DEPTH + 10 + Math.random() * 40,
        passed: false
    });

    // Spawn interval based on physical distance and current speed
    if (score >= 950000) {
        // HELL MODE: nearly impossible, relentless zig-zag
        // Spawns a spike every 70-100 pixels physically. Insanely tight but mathematically possible.
        spawnTimer = (70 + Math.random() * 30) / currentSpeed;
    } else if (score >= 50000) {
        // MID-TO-LATE GAME: "Harder and harder the farther you go"
        const midDifficulty = Math.min(1, (score - 50000) / 900000); // 0.0 to 1.0 from 50k to 950k
        
        // Gap drops from 250px down to 100px as you approach 950k
        const minDistance = 250 - (150 * midDifficulty); 
        const randomRange = 150 - (100 * midDifficulty); // Range shrinks so spikes get tighter and tighter
        spawnTimer = (minDistance + Math.random() * randomRange) / currentSpeed;
    } else {
        // EARLY GAME (0 to 50k): Gentle ramp up
        const difficulty = Math.min(1, score / 50000); // 0.0 to 1.0
        const minDistance = 500 - (250 * difficulty); // 500 -> 250
        const randomRange = 200 - (100 * difficulty); // 200 -> 100
        spawnTimer = (minDistance + Math.random() * randomRange) / currentSpeed;
    }
}

// ════════════════════════════════════════════════════════════════
//  COLLISION – point-in-triangle for the player centre vs spike
// ════════════════════════════════════════════════════════════════

// Returns the three vertices of a spike given its obstacle data
function spikeVerts(ob) {
    if (ob.lane === 0) {
        // Left wall spike: triangle pointing RIGHT
        const x0 = WALL_WIDTH;                    // base top-left
        const y0 = ob.y;
        const x1 = WALL_WIDTH;                    // base bottom-left
        const y1 = ob.y + ob.height;
        const x2 = WALL_WIDTH + ob.depth;         // tip (pointing inward)
        const y2 = ob.y + ob.height / 2;
        return [x0, y0, x1, y1, x2, y2];
    } else {
        // Right wall spike: triangle pointing LEFT
        const baseX = canvas.width - WALL_WIDTH;
        const x0 = baseX;
        const y0 = ob.y;
        const x1 = baseX;
        const y1 = ob.y + ob.height;
        const x2 = baseX - ob.depth;
        const y2 = ob.y + ob.height / 2;
        return [x0, y0, x1, y1, x2, y2];
    }
}

function sign(px, py, ax, ay, bx, by) {
    return (px - bx) * (ay - by) - (ax - bx) * (py - by);
}

function pointInTriangle(px, py, x0, y0, x1, y1, x2, y2) {
    const d1 = sign(px, py, x0, y0, x1, y1);
    const d2 = sign(px, py, x1, y1, x2, y2);
    const d3 = sign(px, py, x2, y2, x0, y0);
    const hasNeg = (d1 < 0) || (d2 < 0) || (d3 < 0);
    const hasPos = (d1 > 0) || (d2 > 0) || (d3 > 0);
    return !(hasNeg && hasPos);
}

function playerHitsSpike(ob) {
    const [x0, y0, x1, y1, x2, y2] = spikeVerts(ob);

    // Check multiple points around the player circle for robust detection
    const cx = player.visualX;
    const cy = player.y;
    const r  = PLAYER_RADIUS - 2; // small forgiveness margin

    // 8 perimeter points + centre
    for (let a = 0; a < Math.PI * 2; a += Math.PI / 4) {
        const px = cx + Math.cos(a) * r;
        const py = cy + Math.sin(a) * r;
        if (pointInTriangle(px, py, x0, y0, x1, y1, x2, y2)) return true;
    }
    return pointInTriangle(cx, cy, x0, y0, x1, y1, x2, y2);
}

// ════════════════════════════════════════════════════════════════
//  NEAR MISS / PERFECT
// ════════════════════════════════════════════════════════════════
function checkNearMiss() {
    let closestDist = Infinity;

    obstacles.forEach(ob => {
        // We just switched AWAY from ob.lane (we're now on the other wall).
        // Only care about spikes on the wall we LEFT.
        if (ob.lane === player.lane) return; // spike is on our NEW wall – irrelevant

        // Vertical overlap / proximity
        const spikeTop    = ob.y;
        const spikeBottom = ob.y + ob.height;
        const py = player.y;

        // Vertical distance: negative means overlapping
        let dist;
        if (py >= spikeTop && py <= spikeBottom) {
            dist = 0; // inside vertical range
        } else {
            dist = Math.min(Math.abs(py - spikeTop), Math.abs(py - spikeBottom));
        }

        if (dist < closestDist) closestDist = dist;
    });

    if (closestDist <= PERFECT_DIST) {
        triggerPerfect();
    } else if (closestDist <= NEAR_MISS_DIST) {
        triggerNearMiss();
    }
}

function triggerNearMiss() {
    playNearMiss();
    score += 5;
}

function triggerPerfect() {
    playPerfect();
    combo++;
    score += 10 * getMultiplier();
    updateUI();
}

// ════════════════════════════════════════════════════════════════
//  PARTICLES
// ════════════════════════════════════════════════════════════════
function spawnParticles(x, y, color) {
    for (let i = 0; i < 60; i++) {
        particles.push({
            x, y,
            vx: (Math.random() - 0.5) * 1500,
            vy: (Math.random() - 0.5) * 1500,
            life: 1.5 + Math.random(),
            color: Math.random() > 0.5 ? '#00ffff' : '#ff00ff'
        });
    }
}

// ════════════════════════════════════════════════════════════════
//  SCORING HELPERS
// ════════════════════════════════════════════════════════════════
function getMultiplier() {
    if (combo >= 20) return 10;
    if (combo >= 10) return 5;
    if (combo >= 5)  return 3;
    if (combo >= 2)  return 2;
    return 1;
}

function updateUI() {
    // Hide DOM elements – we draw everything on canvas now
    scoreDisplay.classList.add('hidden');
    comboDisplay.classList.add('hidden');
}

// ════════════════════════════════════════════════════════════════
//  GAME LIFECYCLE
// ════════════════════════════════════════════════════════════════
function startGame() {
    isPlaying = true;
    score = 0;
    combo = 0;
    maxCombo = 0;
    timeSurvived = 0;
    currentSpeed = baseSpeed;
    obstacles = [];
    particles = [];
    spawnTimer = 1.5; // grace period before first spike
    scrollOffset = 0;

    startScreen.classList.add('hidden');
    gameOverScreen.classList.add('hidden');
    winScreen.classList.add('hidden');
    perfectText.classList.add('hidden');
    perfectText.style.animation = 'none';

    resize();
    setPlayerX(true);
    if (audioCtx.state === 'suspended') audioCtx.resume();
    lastTime = performance.now();
    requestAnimationFrame(loop);
}

function restartGame() { startGame(); }

function gameOver() {
    isPlaying = false;
    playHit();
    container.classList.add('shake');
    setTimeout(() => container.classList.remove('shake'), 300);
    spawnParticles(player.visualX, player.y, '#00ffff');

    gameOverScreen.classList.remove('hidden');
    finalScoreEl.innerText = Math.floor(score);
    finalComboEl.innerText = maxCombo;
}

function triggerWin() {
    isPlaying = false;
    playTone(523, 0.15, 'sine', 0.15);
    setTimeout(() => playTone(659, 0.15, 'sine', 0.15), 100);
    setTimeout(() => playTone(784, 0.15, 'sine', 0.15), 200);
    setTimeout(() => playTone(1047, 0.3, 'sine', 0.15), 300);

    winScreen.classList.remove('hidden');
    winScoreEl.innerText = Math.floor(score).toLocaleString();
    winComboEl.innerText = maxCombo;
    winTimeEl.innerText = Math.floor(timeSurvived);
}

// ════════════════════════════════════════════════════════════════
//  MAIN LOOP
// ════════════════════════════════════════════════════════════════
function loop(timestamp) {
    if (!isPlaying) return;

    let rawDt = (timestamp - lastTime) / 1000;
    // Cap max delta time to 0.1s to prevent huge skips if the game lags or resumes
    if (rawDt > 0.1) rawDt = 0.1;
    
    lastTime = timestamp;
    const dt = rawDt * timeScale;

    timeSurvived += dt;
    score += dt * getMultiplier();

    // Win condition
    if (score >= 1000000) {
        triggerWin();
        return;
    }

    // Speed Curve phases
    if (score >= 950000) {
        // Massive speed jump for Hell mode
        currentSpeed = 2500;
    } else {
        // Base smooth exponential curve
        currentSpeed = baseSpeed * Math.pow(1.04, timeSurvived);
        
        if (score >= 50000) {
            // Mid-game: noticeably faster step up and higher cap
            currentSpeed = Math.max(1300, Math.min(currentSpeed, 1800));
        } else {
            // Early game: gentle speed cap
            currentSpeed = Math.min(currentSpeed, 1100);
        }
    }

    // Smooth player position
    const lerp = Math.min(1, 35 * dt); // faster horizontal snap
    player.visualX += (player.targetX - player.visualX) * lerp;
    
    // Calculate distance to target to create a subtle vertical "arc" (slant) during dash
    const distToTarget = Math.abs(player.targetX - player.visualX);
    const maxDist = canvas.width - (WALL_WIDTH * 2) - (PLAYER_RADIUS * 2);
    // Subtle Y bump: max 12px up in the middle of the dash
    const arcHeight = 12 * Math.sin(Math.PI * (1 - (distToTarget / maxDist)));
    player.visualY = player.y - arcHeight;

    // Spawning
    spawnTimer -= dt;
    if (spawnTimer <= 0) spawnObstacle();

    // Heavy player comet trail
    if (isPlaying) {
        for (let k=0; k<2; k++) {
            particles.push({
                x: player.visualX + (Math.random() - 0.5) * (PLAYER_RADIUS * 1.5),
                y: player.visualY + PLAYER_RADIUS,
                vx: (Math.random() - 0.5) * 60,
                vy: currentSpeed * 0.5 + Math.random() * 150, 
                color: Math.random() > 0.5 ? '#00ffff' : '#ff00ff',
                life: 0.8 + Math.random() * 0.6
            });
        }
    }

    // Wall electric sparks
    if (isPlaying && Math.random() < 0.1) {
        const wallX = Math.random() > 0.5 ? WALL_WIDTH : canvas.width - WALL_WIDTH;
        particles.push({
            x: wallX,
            y: Math.random() * canvas.height,
            vx: (wallX === WALL_WIDTH ? 1 : -1) * (Math.random() * 100),
            vy: (Math.random() - 0.5) * 200,
            color: '#00ffff',
            life: 0.3 + Math.random() * 0.2
        });
    }

    // Scroll offset for perspective grid
    scrollOffset = (scrollOffset + currentSpeed * dt) % 1000;

    // Update obstacles
    for (let i = obstacles.length - 1; i >= 0; i--) {
        const ob = obstacles[i];
        ob.y += currentSpeed * dt;

        // Collision
        if (ob.lane === player.lane && playerHitsSpike(ob)) {
            gameOver();
        }

        // Passed
        if (!ob.passed && ob.y > player.y + PLAYER_RADIUS) {
            ob.passed = true;
            combo++;
            if (combo > maxCombo) maxCombo = combo;
        }

        // Remove offscreen
        if (ob.y > canvas.height + 50) obstacles.splice(i, 1);
    }

    updateUI();
    draw();

    if (isPlaying) requestAnimationFrame(loop);
    else draw(); // one last frame
}

// ════════════════════════════════════════════════════════════════
//  DRAW
// ════════════════════════════════════════════════════════════════
function draw() {
    const w = canvas.width;
    const h = canvas.height;

    // ── Background (Deep Cyber Tunnel) ──
    const bgGrad = ctx.createLinearGradient(0, 0, 0, h);
    bgGrad.addColorStop(0, '#02000a');
    bgGrad.addColorStop(1, '#110022');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, w, h);

    // ── Giant Background Rings ──
    ctx.strokeStyle = 'rgba(255, 0, 255, 0.05)';
    ctx.lineWidth = 4;
    const time = performance.now() * 0.001;
    ctx.beginPath();
    ctx.arc(w/2, h/2, 250 + Math.sin(time)*20, 0, Math.PI*2);
    ctx.stroke();
    
    ctx.beginPath();
    ctx.arc(w/2, h/2, 400 + Math.cos(time*0.8)*30, 0, Math.PI*2);
    ctx.stroke();

    // ── Perspective Grid ────
    ctx.strokeStyle = 'rgba(0, 255, 255, 0.1)';
    ctx.lineWidth = 1.5;
    
    // Vertical diverging lines
    const centerX = w / 2;
    for (let i = 0; i <= 10; i++) {
        const offset = (i - 5) * 40;
        ctx.beginPath();
        ctx.moveTo(centerX, 0); 
        ctx.lineTo(centerX + offset * 4, h); 
        ctx.stroke();
    }
    
    // Horizontal accelerating lines
    for (let i = 0; i < 25; i++) {
        const yBase = (scrollOffset + i * 40) % 1000; 
        const perspectiveY = (yBase * yBase) / 1000; 
        if (perspectiveY < h && perspectiveY > 0) {
            ctx.beginPath();
            ctx.moveTo(WALL_WIDTH, perspectiveY);
            ctx.lineTo(w - WALL_WIDTH, perspectiveY);
            ctx.stroke();
        }
    }

    // ── Draw Cyber Walls ───────────────────────
    ctx.fillStyle = '#050508'; 
    ctx.fillRect(0, 0, WALL_WIDTH, h);
    ctx.fillRect(w - WALL_WIDTH, 0, WALL_WIDTH, h);

    // Glowing edge trim (Electric cyan)
    ctx.shadowBlur = 20;
    ctx.shadowColor = '#00ffff';
    ctx.strokeStyle = '#00ffff';
    ctx.lineWidth = 4;

    // Left edge
    ctx.beginPath();
    ctx.moveTo(WALL_WIDTH, 0);
    ctx.lineTo(WALL_WIDTH, h);
    ctx.stroke();
    // Right edge
    ctx.beginPath();
    ctx.moveTo(w - WALL_WIDTH, 0);
    ctx.lineTo(w - WALL_WIDTH, h);
    ctx.stroke();
    ctx.shadowBlur = 0;

    // ── Draw Pink Crystal Spikes ────────
    obstacles.forEach(ob => {
        const [x0, y0, x1, y1, x2, y2] = spikeVerts(ob);

        // Dark metal base
        ctx.fillStyle = '#110022';
        ctx.beginPath();
        ctx.moveTo(x0, y0);
        ctx.lineTo(x2, y2);
        ctx.lineTo(x1, y1);
        ctx.closePath();
        ctx.fill();

        // Neon pink outline
        ctx.shadowBlur = 15;
        ctx.shadowColor = '#ff00ff';
        ctx.strokeStyle = '#ff00ff';
        ctx.lineWidth = 2.5;
        ctx.stroke();

        // Inner white-hot pink energy core
        ctx.fillStyle = '#ffffff';
        ctx.shadowBlur = 20;
        ctx.shadowColor = '#ff00ff';
        ctx.beginPath();
        // Jagged inner crystal
        const coreSize = 0.3 + Math.random()*0.1;
        const cx = (x0 + x1 + x2) / 3;
        const cy = (y0 + y1 + y2) / 3;
        ctx.moveTo(cx + (x0 - cx) * coreSize, cy + (y0 - cy) * coreSize);
        ctx.lineTo(cx + (x2 - cx) * coreSize, cy + (y2 - cy) * coreSize);
        ctx.lineTo(cx + (x1 - cx) * coreSize, cy + (y1 - cy) * coreSize);
        ctx.closePath();
        ctx.fill();
        
        ctx.shadowBlur = 0;
    });

    // ── Draw Particles ────────────────────────
    for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        const pdt = isPlaying ? 0.016 * timeScale : 0.016;
        p.x += p.vx * pdt;
        p.y += p.vy * pdt;
        p.life -= pdt * 2;
        ctx.globalAlpha = Math.max(0, p.life);
        ctx.fillStyle = p.color;
        
        ctx.shadowBlur = 8;
        ctx.shadowColor = p.color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
        ctx.fill();
        
        if (p.life <= 0) particles.splice(i, 1);
    }
    ctx.globalAlpha = 1;
    ctx.shadowBlur = 0;

    // ── Draw Player ───────────────────────────
    if (isPlaying || particles.length > 0) {
        if (isPlaying) {
            const px = player.visualX;
            const py = player.visualY || player.y;

            // Massive Cyan Glow
            ctx.shadowBlur = 25 + getMultiplier() * 5;
            ctx.shadowColor = '#00ffff';
            ctx.fillStyle = '#00ffff';

            ctx.beginPath();
            ctx.arc(px, py, PLAYER_RADIUS, 0, Math.PI * 2);
            ctx.fill();

            // Inner bright core
            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.arc(px, py, PLAYER_RADIUS * 0.5, 0, Math.PI * 2);
            ctx.fill();

            ctx.shadowBlur = 0;
        }
    }

    // ── Sci-Fi HUD (drawn LAST, on top of everything) ──────────
    drawHUD(w, h);
}

// ════════════════════════════════════════════════════════════════
//  SCI-FI HUD
// ════════════════════════════════════════════════════════════════
function drawHUD(w, h) {
    const cx = w / 2;
    const scoreStr = String(Math.floor(score));
    const mult = getMultiplier();

    // ── Score: big centred number ──────
    ctx.save();
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    // Outer glow layer
    ctx.font = 'bold 72px "Courier New", monospace';
    ctx.shadowBlur = 30;
    ctx.shadowColor = 'rgba(0,255,255,0.5)';
    ctx.fillStyle = 'rgba(0,255,255,0.12)';
    ctx.fillText(scoreStr, cx, 60);

    // Main score text
    ctx.shadowBlur = 15;
    ctx.shadowColor = '#00ffff';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(scoreStr, cx, 60);
    ctx.shadowBlur = 0;

    // ── Sci-fi bracket frame around score ──
    const tw = ctx.measureText(scoreStr).width;
    const pad = 28;
    const frameL = cx - tw / 2 - pad;
    const frameR = cx + tw / 2 + pad;
    const frameT = 22;
    const frameB = 98;
    const corner = 12;

    ctx.strokeStyle = 'rgba(0,255,255,0.35)';
    ctx.lineWidth = 1.5;
    ctx.shadowBlur = 6;
    ctx.shadowColor = 'rgba(0,255,255,0.3)';

    // Top-left corner
    ctx.beginPath();
    ctx.moveTo(frameL, frameT + corner);
    ctx.lineTo(frameL, frameT);
    ctx.lineTo(frameL + corner, frameT);
    ctx.stroke();
    // Top-right corner
    ctx.beginPath();
    ctx.moveTo(frameR - corner, frameT);
    ctx.lineTo(frameR, frameT);
    ctx.lineTo(frameR, frameT + corner);
    ctx.stroke();
    // Bottom-left corner
    ctx.beginPath();
    ctx.moveTo(frameL, frameB - corner);
    ctx.lineTo(frameL, frameB);
    ctx.lineTo(frameL + corner, frameB);
    ctx.stroke();
    // Bottom-right corner
    ctx.beginPath();
    ctx.moveTo(frameR - corner, frameB);
    ctx.lineTo(frameR, frameB);
    ctx.lineTo(frameR, frameB - corner);
    ctx.stroke();

    // Thin horizontal accent lines
    ctx.strokeStyle = 'rgba(0,255,255,0.15)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(frameL + corner + 4, frameT);
    ctx.lineTo(frameR - corner - 4, frameT);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(frameL + corner + 4, frameB);
    ctx.lineTo(frameR - corner - 4, frameB);
    ctx.stroke();

    ctx.shadowBlur = 0;

    // ── Multiplier badge ──────────────
    if (mult > 1) {
        const multStr = `x${mult}`;
        ctx.font = 'bold 28px "Courier New", monospace';
        ctx.shadowBlur = 10;
        ctx.shadowColor = '#00ffff';

        // Pulse alpha with time
        const pulse = 0.7 + 0.3 * Math.sin(performance.now() * 0.008);
        ctx.fillStyle = `rgba(0,255,255,${pulse})`;
        ctx.fillText(multStr, cx, 120);
        ctx.shadowBlur = 0;
    }

    // ── "COMBO" label left wall ───────
    if (combo > 0) {
        ctx.font = '12px "Courier New", monospace';
        ctx.fillStyle = 'rgba(255,255,255,0.35)';
        ctx.textAlign = 'left';
        ctx.fillText('COMBO', WALL_WIDTH + 8, 30);
        ctx.font = 'bold 22px "Courier New", monospace';
        ctx.fillStyle = '#00ffff';
        ctx.fillText(String(combo), WALL_WIDTH + 8, 54);
    }


    ctx.restore();
}

// ═══ Boot ═══
resize();
draw();

// Instantly kill the player if they leave the tab
document.addEventListener('visibilitychange', () => {
    if (document.hidden && isPlaying) {
        triggerGameOver();
    }
});
