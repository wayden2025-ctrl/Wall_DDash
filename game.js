
// --- Audio System ---
let playlist = [
    'monume-synthwave-retro-80s-498055.m4a',
    'monume-cyberpunk-547930.m4a',
    'delosound-inspiring-motivation-synthwave-398285.m4a',
    'the_mountain-electronic-retrowave-132335.m4a'
];

// Shuffle the playlist once on load
for (let i = playlist.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [playlist[i], playlist[j]] = [playlist[j], playlist[i]];
}

let bgMusic = new Audio();
bgMusic.volume = 0.5;
let currentTrackIndex = 0;

function playNextTrack() {
    bgMusic.src = playlist[currentTrackIndex];
    bgMusic.play().catch(e => console.log("Audio play blocked by browser:", e));
    
    // Cycle to next song in the shuffled playlist
    currentTrackIndex = (currentTrackIndex + 1) % playlist.length;
}

bgMusic.addEventListener('ended', () => {
    // 3 seconds delay before next song
    setTimeout(playNextTrack, 3000);
});

let audioStarted = false;
function initAudio() {
    if (!audioStarted && isPlaying) {
        audioStarted = true;
        playNextTrack();
    }
}

// Add interaction listeners but only start if game is playing
window.addEventListener('click', initAudio);
window.addEventListener('keydown', initAudio);
window.addEventListener('touchstart', initAudio);


const canvas = document.getElementById('game-canvas');
const ctx = canvas.getContext('2d');
const container = document.getElementById('game-container');

const spikeVariants = [
    { src: 'spike_small.png', width: 61, height: 86, scale: 1.0 },
    { src: 'spike_large.png', width: 103, height: 124, scale: 0.9 }
].map(v => {
    const img = new Image();
    img.src = v.src;
    return {
        img,
        width: v.width * v.scale,
        height: v.height * v.scale
    };
});



// --- Orb Customization ---

window.updateOrbSelection = function(id, color, src) {
    selectedOrbId = id;
    selectedOrbColor = color;
    if (id > 0) {
        customOrbImage = new Image();
        customOrbImage.src = src;
    } else {
        customOrbImage = null;
    }
};

let selectedOrbId = parseInt(localStorage.getItem('selectedOrbId') || '0', 10);
let selectedOrbColor = localStorage.getItem('selectedOrbColor') || '#ff00ff';

function getVaryingColor(hex) {
    if (!hex || hex.length !== 7) return hex;
    let r = parseInt(hex.slice(1,3), 16);
    let g = parseInt(hex.slice(3,5), 16);
    let b = parseInt(hex.slice(5,7), 16);
    
    const vary = () => Math.floor(Math.random() * 100 - 50); // +/- 50 variance for noticeable differences
    r = Math.min(255, Math.max(0, r + vary()));
    g = Math.min(255, Math.max(0, g + vary()));
    b = Math.min(255, Math.max(0, b + vary()));
    
    return `rgba(${r}, ${g}, ${b}, 0.8)`;
}

let customOrbImage = null;

if (selectedOrbId > 0) {
    customOrbImage = new Image();
    customOrbImage.src = 'orb_' + selectedOrbId + '.png';
}

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
const publisherContent = document.getElementById('publisher-content');

// ─── Layout Constants ──────────────────────────────────────────
const WALL_WIDTH = 6;          // thickness of each white wall
const SPIKE_BASE = 30;         // spike height along the wall (vertical size)
const SPIKE_DEPTH = 50;        // how far the spike juts inward
const PLAYER_RADIUS = 18;      // player is a small circle on the wall

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

initRevives();

function revivePlayer() {
    if (revivesLeft <= 0) return;
    
    revivesLeft--;
    localStorage.setItem('revivesLeft', revivesLeft.toString());
    
    // Clear screen spin
    screenSpinTimer = 0;
    screenFlipTimer = 0;
    canvas.style.transform = 'translate(-50%, -50%) rotate(0rad) scale(1)';
    
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
    
    // We do NOT call a separate revive loop. 
    // The main loop() will handle the revive countdown.
}

// ─── Player ────────────────────────────────────────────────────
const player = {
    lane: 0,     // 0 = left wall, 1 = right wall
    y: 0,        // set on resize (near bottom)
    x: 0,        // computed from lane
    targetX: 0,
    visualX: 0
};

// ─── Obstacles & Particles ─────────────────────────────────────
let obstacles = [];
    player.history = [];
let particles = [];
let spawnTimer = 0;
const SPAWN_INTERVAL = 0.45;  // spawn every 0.45s – dense but playable
const MIN_SPIKE_GAP = 50;     // minimum vertical px between any two spikes on the same wall
let lastSpawnLane = -1;        // track last wall to alternate

// ─── Near-miss / perfect thresholds (vertical px) ──────────────
const NEAR_MISS_DIST = 90;
const PERFECT_DIST = 35;

// ─── Rendering & Parallax ──────────────────────────
let scrollOffset = 0;
let screenShakeTime = 0;
let screenShakeIntensity = 0;
let screenSpinTimer = 0;
let screenSpinStartAngle = 0;
let angleDeg = 0;
let isReversed = false;
let screenFlipTimer = 0;
let screenFlipMaxTimer = 0;
let freezeTime = 0;

// ── Neon Hacker Matrix Rain Initialization ──
const matrixChars = "0179%#@&?!/\[]{}<>XKRVNZ";
const matrixColors = ['#ff0055', '#ff00ff', '#8800ff', '#0088ff', '#ff00aa'];
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
} // Sparse enough to not lag, dense enough to look cool

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

let ambientParticles = [];
for (let i = 0; i < 30; i++) {
    ambientParticles.push({
        x: Math.random(),
        y: Math.random(),
        speed: 0.05 + Math.random() * 0.1,
        size: 1 + Math.random() * 3,
        color: Math.random() > 0.5 ? '#ff0055' : '#0088ff'
    });
}


// ════════════════════════════════════════════════════════════════
//  RESIZE
// ════════════════════════════════════════════════════════════════
function resize() {
    canvas.width  = container.clientWidth;
    canvas.height = container.clientHeight;
    
    // Ensure canvas is absolutely centered in the container so transform: rotate spins around the center
    canvas.style.position = 'absolute';
    canvas.style.top = '50%';
    canvas.style.left = '50%';
    // The translate(-50%, -50%) is applied in the update loop along with rotation and scale.
    // Set initial transform so it's centered before update runs.
    canvas.style.transform = `translate(-50%, -50%) rotate(${typeof screenRotation !== 'undefined' ? screenRotation : 0}rad) scale(1)`;
    canvas.style.transformOrigin = 'center center';
    player.y = canvas.height - 220;
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
    

    // Impact dash burst
    for(let i=0; i<15; i++) {
        particles.push({ size: 2 + Math.random()*3,
            x: player.visualX,
            y: player.visualY,
            vx: (Math.random() - 0.5) * 300,
            vy: (Math.random() - 0.5) * 300,
            color: '#0088ff',
            life: 0.4 + Math.random() * 0.3
        });
    }
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
let nextLane = Math.random() < 0.5 ? 0 : 1;
let sameSideCount = 0;

function spawnObstacle() {
    let yPos = -150; // spawn fully offscreen
    let lane = nextLane;

    // Pick a random variant
    const variant = spikeVariants[Math.floor(Math.random() * spikeVariants.length)];
    // Randomize the size of the specific spike chosen so they aren't all the same size
    const randomScale = 0.7 + Math.random() * 0.7; // Scale between 0.7x and 1.4x
    const spikeHeight = variant.height * randomScale;
    const spikeDepth = variant.width * randomScale;

    const rand = Math.random();
    let type = 'spike';
    if (rand < 0.10) {
        type = 'spiral';
    } else if (rand < 0.20) {
        type = 'flipper';
    } else if (rand < 0.30) {
        type = 'wormhole';
    }
    
    if (isReversed) {
        yPos = canvas.height + 150;
    }

    if (type === 'spiral' || type === 'flipper' || type === 'wormhole') {
        yPos += (isReversed ? 500 : -500); // Spawns way offscreen, creating a massive gap before the special
        
        // Floating slightly off the wall, radius ~30
        obstacles.push({
            type: type,
            lane,
            y: yPos,
            radius: 30,
            rotation: 0, // Used for drawing animation
            passed: false
        });
    } else {
        obstacles.push({
            type: 'spike',
            lane,
            y: yPos,
            height: spikeHeight,
            depth: spikeDepth,
            variant: variant,
            passed: false
        });
    }

    // Determine the lane for the NEXT spike
    // Use true 50/50 randomness for the lane to avoid repetitive "grouping" patterns
    let switchLanes = Math.random() < 0.5;
    
    // Prevent more than 4 on the same side so it doesn't get boring
    if (sameSideCount >= 4) {
        switchLanes = true;
    }

    let physicalDistance;

    if (switchLanes) {
        nextLane = lane === 0 ? 1 : 0;
        sameSideCount = 0;
        
        // When switching lanes, we MUST guarantee enough vertical space for the player to diagonally dash across
        // The required space is: height of the current spike + distance player travels forward during dash + small buffer
        // Player dash takes roughly 0.18 seconds to cross the screen safely at these speeds
        let dashTimeDistance = currentSpeed * 0.18; 
        let safeBuffer = 80; 
        
        // Total physical distance before the NEXT spike appears on the other side
        physicalDistance = spikeHeight + dashTimeDistance + safeBuffer + (Math.random() * 150);
    } else {
        nextLane = lane;
        sameSideCount++;
        
        // NO OVERLAPPING: distance to the next spike MUST be at least the height of this spike + a small gap.
        physicalDistance = spikeHeight + 10 + Math.random() * 50; 
    }
    
    if (type === 'spiral' || type === 'flipper') {
        // Enforce a massive gap AFTER the spiral/flipper so the player has time to recover while spinning.
        // We add 1000 because we shifted yPos up by 500, and we want another 500 gap after it.
        physicalDistance += 1000; 
    }

    // Timer is distance divided by speed
    spawnTimer = physicalDistance / currentSpeed;
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

    // Update active particles (trail, sparks, ambient)
    for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx * dt;
        p.y += p.vy * dt;
        if (p.life !== undefined) {
            p.life -= dt;
            if (p.life <= 0) particles.splice(i, 1);
        } else {
            // Fallback for particles without life (if any)
            if (p.y > canvas.height + 50 || p.y < -50 || p.x < -50 || p.x > canvas.width + 50) {
                particles.splice(i, 1);
            }
        }
    }

    updateUI();
}

// ════════════════════════════════════════════════════════════════
//  PARTICLES
// ════════════════════════════════════════════════════════════════
function spawnShatterParticles(x, y, color) {
    for (let i = 0; i < 50; i++) {
        particles.push({ 
            size: 4 + Math.random() * 8,
            x: x, 
            y: y,
            vx: (Math.random() - 0.5) * 2000,
            vy: (Math.random() - 0.5) * 2000,
            life: 2.0 + Math.random(),
            color: color || selectedOrbColor,
            isShatter: true,
            angle: Math.random() * Math.PI * 2,
            vAngle: (Math.random() - 0.5) * 15
        });
    }
}
function spawnImpactEmbers(x, y, dir) {
    for (let i = 0; i < 15; i++) {
        particles.push({
            size: 2 + Math.random() * 4,
            x: x,
            y: y,
            vx: dir * (200 + Math.random() * 400),
            vy: (Math.random() - 0.5) * 600,
            life: 0.3 + Math.random() * 0.3,
            color: '#fff',
            isEmber: true
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
    initAudio();
    isPlaying = true;
    score = 0;
    combo = 0;
    maxCombo = 0;
    timeSurvived = 0;
    currentSpeed = baseSpeed;
    obstacles = [];
    player.history = [];
    particles = [];
    spawnTimer = 1.5; // grace period before first spike
    scrollOffset = 0;
    
    // Clear screen spin, flip, and reverse
    screenSpinTimer = 0;
    screenFlipTimer = 0;
    isReversed = false;
    canvas.style.transform = 'translate(-50%, -50%) rotate(0rad) scale(1)';

    startScreen.classList.add('hidden');
    gameOverScreen.classList.add('hidden');
    winScreen.classList.add('hidden');
    perfectText.classList.add('hidden');
    perfectText.style.animation = 'none';
    
    if (publisherContent) {
        publisherContent.style.display = 'none';
    }

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
    freezeTime = 0.15; // Hit stop for 150ms
    screenShakeTime = 0.4; // Reduced shake duration
    screenShakeIntensity = 6; // Very subtle shake magnitude
    spawnShatterParticles(player.visualX, player.y, selectedOrbColor);
    
    // Immediately stop the screen from spinning if they died
    screenSpinTimer = 0;
    screenFlipTimer = 0;
    canvas.style.transform = 'translate(-50%, -50%) rotate(0rad) scale(1)';
    
    // We do NOT show the UI here anymore; it is handled in the loop after the freeze.
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
    let rawDt = (timestamp - lastTime) / 1000;
    // Cap max delta time to 0.1s to prevent huge skips
    if (rawDt > 0.1) rawDt = 0.1;
    
    lastTime = timestamp;

    if (isReviving) {
        reviveTimer -= rawDt;
        draw();
        
        ctx.save();
        ctx.fillStyle = `rgba(0, 255, 255, 1)`;
        ctx.font = 'bold 150px Courier New';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.shadowBlur = 30;
        ctx.shadowColor = '#ff00ff';
        const num = Math.ceil(reviveTimer);
        if (num > 0) {
            const scale = 1 + (num - reviveTimer);
            ctx.translate(canvas.width/2, canvas.height/2);
            ctx.scale(scale, scale);
            ctx.fillText(num, 0, 0);
        }
        ctx.restore();
        
        if (reviveTimer <= 0) {
            isReviving = false;
            isPlaying = true;
        }
        requestAnimationFrame(loop);
        return;
    }
    
    // Hit stop logic
    if (freezeTime > 0) {
        freezeTime -= rawDt;
        draw();
        if (freezeTime > 0) {
            requestAnimationFrame(loop);
            return;
        } else {
            // Once freeze ends, if not playing, we wait 1s for the explosion then show game over UI
            if (!isPlaying) {
                setTimeout(() => {
                    if (!isPlaying) {
                        gameOverScreen.classList.remove('hidden');
                        finalScoreEl.innerText = Math.floor(score);
                        finalComboEl.innerText = maxCombo;
                        const reviveBtn = document.getElementById('revive-btn');
                        if (reviveBtn) {
                            if (revivesLeft > 0) {
                                reviveBtn.innerHTML = `REVIVE (${revivesLeft} Left)<br><span style="font-size:14px; color:#eee; font-weight:normal; text-shadow:none; letter-spacing:1px; margin-top:5px; display:block;">Free revives refresh every day!</span>`;
                                reviveBtn.onclick = revivePlayer;
                                reviveBtn.style.background = 'linear-gradient(45deg, #00ffaa, #0088ff)';
                                reviveBtn.style.boxShadow = '0 0 20px rgba(0,255,170,0.6)';
                            } else {
                                reviveBtn.innerHTML = `BUY MORE REVIVES<br><span style="font-size:14px; color:#eee; font-weight:normal; text-shadow:none; letter-spacing:1px; margin-top:5px; display:block;">Or wait until tomorrow for 3 free!</span>`;
                                reviveBtn.onclick = () => document.getElementById('store-modal').style.display = 'flex';
                                reviveBtn.style.background = 'linear-gradient(45deg, #ffaa00, #ff0055)';
                                reviveBtn.style.boxShadow = '0 0 20px rgba(255,170,0,0.6)';
                            }
                        }
                    }
                }, 1000); // Wait 1 second for the explosion to play out!
            }
            // Need to reset lastTime so we don't get a huge jump after freeze
            lastTime = performance.now();
            requestAnimationFrame(loop);
            return;
        }
    }
    
    const dt = rawDt * timeScale;

    if (isPlaying) {
        timeSurvived += dt;
        score += dt * getMultiplier();

        // Win condition
        if (score >= 1000000) {
            triggerWin();
            return;
        }

        // Speed Curve
        currentSpeed = baseSpeed + (timeSurvived * 15);

        // Smooth player position
        player.targetY = isReversed ? canvas.height * 0.3 : canvas.height - 220;
        
        const lerpX = Math.min(1, 50 * dt); // extremely fast snap
        player.visualX += (player.targetX - player.visualX) * lerpX;
        
        const lerpY = Math.min(1, 3 * dt); // smooth transition for Y
        player.y += (player.targetY - player.y) * lerpY;
        
        // Calculate distance to target to create a subtle vertical "arc" (slant) during dash
        const distToTarget = Math.abs(player.targetX - player.visualX);
        
        // Impact Embers and Micro Shake on landing
        if (distToTarget > 10) {
            player.isDashing = true;
        } else if (player.isDashing && distToTarget <= 10) {
            player.isDashing = false;
            // Minor hit stop and screen shake on dash landing
            screenShakeTime = 0.1;
            screenShakeIntensity = 2;
            // Determine direction of embers (away from wall)
            const dir = player.lane === 0 ? 1 : -1; 
            spawnImpactEmbers(player.visualX, player.visualY, dir);
        }
        const maxDist = canvas.width - (WALL_WIDTH * 2) - (PLAYER_RADIUS * 2);
        // Subtle Y bump: max 12px up in the middle of the dash
        const arcHeight = 12 * Math.sin(Math.PI * (1 - (distToTarget / maxDist)));
        player.visualY = player.y - arcHeight;
        player.history = player.history || [];
        player.history.push({x: player.visualX, y: player.visualY});
        if (player.history.length > 8) player.history.shift();

        // Player trail particles
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

        // Spawning
        spawnTimer -= dt;
        if (spawnTimer <= 0) spawnObstacle();

        // Ambient environment particles (dust, sparks, light motes)
        if (Math.random() < 0.8) {
            particles.push({ size: 2 + Math.random()*3,
                x: Math.random() * canvas.width,
                y: canvas.height + 20, // start slightly offscreen bottom
                vx: (Math.random() - 0.5) * 20,
                vy: -currentSpeed * (0.1 + Math.random() * 0.2), // float up slowly relative to speed
                color: Math.random() > 0.5 ? 'rgba(0, 255, 255, 0.4)' : 'rgba(255, 0, 255, 0.4)',
                life: 1.5 + Math.random() * 1.0,
                isAmbient: true
            });
        }

        // Wall electric sparks
        if (Math.random() < 0.2) {
            const wallX = Math.random() > 0.5 ? WALL_WIDTH : canvas.width - WALL_WIDTH;
            particles.push({ size: 2 + Math.random()*3,
                x: wallX,
                y: Math.random() * canvas.height,
                vx: (wallX === WALL_WIDTH ? 1 : -1) * (Math.random() * 100),
                vy: (Math.random() - 0.5) * 200,
                color: '#0088ff',
                life: 0.4 + Math.random() * 0.3
            });
        }
        
        // Update obstacles
        for (let i = obstacles.length - 1; i >= 0; i--) {
            const ob = obstacles[i];
            ob.y += (isReversed ? -1 : 1) * currentSpeed * dt;
            
            if (ob.type === 'spiral' || ob.type === 'flipper' || ob.type === 'wormhole') {
                ob.rotation += 5 * dt;
            }

            // Collision
            if (ob.lane === player.lane) {
                if (ob.type === 'spiral' || ob.type === 'flipper' || ob.type === 'wormhole') {
                    // Simple circle collision
                    const obX = ob.lane === 0 ? WALL_WIDTH + ob.radius + 15 : canvas.width - WALL_WIDTH - ob.radius - 15;
                    const obY = ob.y;
                    const dx = player.visualX - obX;
                    const dy = player.y - obY;
                    const dist = Math.sqrt(dx*dx + dy*dy);
                    
                    if (dist < (PLAYER_RADIUS + ob.radius)) {
                        const hitType = ob.type;
                        obstacles.splice(i, 1);
                        
                        if (hitType === 'wormhole') {
                            isReversed = !isReversed; // Toggle gravity
                            screenShakeIntensity = 4;
                            screenShakeTime = 0.2;
                            
                            // Clear all existing obstacles (spikes, spirals, flippers, etc) to prevent unfair deaths or double-toggles
                            for (let k = obstacles.length - 1; k >= 0; k--) {
                                obstacles.splice(k, 1);
                                if (k < i) {
                                    i--; // Adjust outer loop index
                                }
                            }
                        } else if (hitType === 'spiral') {
                            screenSpinTimer = 5.0; // 5 seconds of spin
                            screenSpinStartAngle = angleDeg; // Capture current angle (could be 90 if flipped)
                            screenFlipTimer = 0; // Cancel any active flip
                            screenFlipMaxTimer = 0;
                        } else {
                            if (screenFlipTimer > 0) {
                                // If already flipped, extend the timers to avoid re-triggering the start animation
                                screenFlipTimer += 5.0;
                                screenFlipMaxTimer += 5.0;
                            } else {
                                screenFlipTimer = 5.0; 
                                screenFlipMaxTimer = 5.0;
                            }
                            screenSpinTimer = 0; // Cancel any active spin
                        }
                        
                        let soundFreq = 500;
                        if (hitType === 'spiral') soundFreq = 300;
                        if (hitType === 'wormhole') soundFreq = 150;
                        playTone(soundFreq, 0.3, 'sawtooth', 0.5); // Glitch sound
                        score += 100; // Bonus points for risk
                        
                        // Spawn glitch particles
                        for (let j = 0; j < 30; j++) {
                            particles.push({
                                size: 2 + Math.random() * 4,
                                x: obX,
                                y: obY,
                                vx: (Math.random() - 0.5) * 800,
                                vy: (Math.random() - 0.5) * 800,
                                life: 1.0,
                                color: hitType === 'spiral' ? '#ff0055' : (hitType === 'wormhole' ? '#00ffff' : '#00ff55')
                            });
                        }
                        continue;
                    }
                } else if (playerHitsSpike(ob)) {
                    gameOver();
                }
            }

            // Passed
            const hasPassed = isReversed ? (ob.y < player.y - PLAYER_RADIUS) : (ob.y > player.y + PLAYER_RADIUS);
            if (!ob.passed && hasPassed) {
                ob.passed = true;
                combo++;
                if (combo > maxCombo) maxCombo = combo;
            }

            // Remove offscreen
            if (isReversed) {
                if (ob.y < -200) obstacles.splice(i, 1);
            } else {
                if (ob.y > canvas.height + 50) obstacles.splice(i, 1);
            }
        }
    } // end if (isPlaying)

    // Update Shapes
    bgObjects.forEach(bg => {
        bg.y += (isReversed ? -1 : 1) * currentSpeed * dt * bg.speed * 0.001;
        
        if (isReversed) {
            if (bg.y * canvas.height < -bg.height - 50) {
                bg.y = (canvas.height + 50) / canvas.height;
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
        } else {
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
        }
    });

    // Update Matrix Streams
    matrixStreams.forEach(stream => {
        stream.y += (isReversed ? -1 : 1) * currentSpeed * dt * stream.speed * 0.001;
        
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
        if (isReversed) {
            if (stream.y + approxStreamHeight < 0.0) {
                Object.assign(stream, createMatrixStream(false));
                stream.y = 1.0 + approxStreamHeight;
            }
        } else {
            if (stream.y - approxStreamHeight > 1.0) {
                // Respawn
                Object.assign(stream, createMatrixStream(false));
            }
        }
    });

    // Screen Shake
    if (screenShakeTime > 0) {
        screenShakeTime -= dt;
    }

    // Screen Spin Mechanic (Corrupted Spiral) & Screen Flip (Flipper)
    angleDeg = 0;
    if (screenFlipTimer > 0) {
        screenFlipTimer -= rawDt;
        if (screenFlipTimer <= 0) {
            screenFlipTimer = 0;
            angleDeg = 0;
        } else {
            // Smoothly rotate to 90 degrees over the first 1 second, hold for remaining, and rotate back over the last 1 second
            const elapsed = screenFlipMaxTimer - screenFlipTimer;
            if (elapsed <= 1.0) {
                // Smooth easing to 90
                const progress = elapsed / 1.0;
                angleDeg = Math.sin((progress * Math.PI) / 2) * 90;
            } else if (screenFlipTimer <= 1.0) {
                // Smooth easing back to 0 (last 1 second of whatever the max timer is)
                const progress = 1.0 - screenFlipTimer;
                // Using cos goes from 1 to 0 smoothly as progress goes from 0 to 1
                angleDeg = Math.cos((progress * Math.PI) / 2) * 90;
            } else {
                // Hold at 90
                angleDeg = 90;
            }
        }
    } else if (screenSpinTimer > 0) {
        screenSpinTimer -= rawDt; // independent of timeScale
        if (screenSpinTimer <= 0) {
            screenSpinTimer = 0;
            angleDeg = 0;
        } else {
            // Spin to 360 degrees over 5 seconds from the starting angle
            const progress = 1.0 - (screenSpinTimer / 5.0);
            const distance = 360 - screenSpinStartAngle;
            angleDeg = screenSpinStartAngle + (progress * distance);
        }
    }
        
        // Convert angle to radians for math
        const angleRad = angleDeg * (Math.PI / 180);
        
        // Calculate Bounding Box of the rotated canvas
        const absCos = Math.abs(Math.cos(angleRad));
        const absSin = Math.abs(Math.sin(angleRad));
        const boundingW = canvas.width * absCos + canvas.height * absSin;
        const boundingH = canvas.width * absSin + canvas.height * absCos;
        
        // Calculate scale to fit exactly inside window viewport
        // (to prevent corners from clipping off the physical screen)
        const scaleX = window.innerWidth / boundingW;
        const scaleY = window.innerHeight / boundingH;
        let scale = Math.min(scaleX, scaleY);
        
        // We only scale down (scale < 1.0), we never scale up
        if (scale > 1.0) scale = 1.0;
        
        // Apply rotation and scaling strictly to the canvas, NOT the container!
        // The container holds the UI, so UI stays upright.
        canvas.style.transform = `translate(-50%, -50%) rotate(${angleDeg}deg) scale(${scale})`;

    // Scroll offset for perspective grid
    scrollOffset = (scrollOffset + currentSpeed * dt) % 1000;

    // Update active particles (trail, sparks, ambient, shatter, embers)
    for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx * dt;
        p.y += p.vy * dt;
        
        if (p.isShatter) {
            p.angle += p.vAngle * dt;
            // Bounce off walls
            if (p.x < WALL_WIDTH) {
                p.x = WALL_WIDTH;
                p.vx *= -0.6;
            } else if (p.x > canvas.width - WALL_WIDTH) {
                p.x = canvas.width - WALL_WIDTH;
                p.vx *= -0.6;
            }
        }

        if (p.life !== undefined) {
            p.life -= dt;
            if (p.life <= 0) particles.splice(i, 1);
        } else {
            // Fallback for particles without life (if any)
            if (p.y > canvas.height + 50 || p.y < -50 || p.x < -50 || p.x > canvas.width + 50) {
                particles.splice(i, 1);
            }
        }
    }

    updateUI();
    draw();

    // Keep running the loop even if not playing, to animate particles!
    requestAnimationFrame(loop);
}

// ════════════════════════════════════════════════════════════════
//  DRAW
// ════════════════════════════════════════════════════════════════
function draw() {
    const w = canvas.width;
    const h = canvas.height;

    ctx.save();
    
    // Apply camera shake
    if (screenShakeTime > 0) {
        const shakeX = (Math.random() - 0.5) * screenShakeIntensity;
        const shakeY = (Math.random() - 0.5) * screenShakeIntensity;
        ctx.translate(shakeX, shakeY);
    }

    // ── Layer 1: Background (Deep Cyber Void) ──
    const bgGrad = ctx.createLinearGradient(0, 0, 0, h);
    bgGrad.addColorStop(0, '#0b001a'); // deep dark violet top
    bgGrad.addColorStop(1, '#1a0033'); // slightly brighter magenta-purple bottom
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, w, h);

    // ── Background Shapes ──
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

    // ── Matrix Code Rain ──
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
    
    // ── Layer 4: Atmospheric FX (Drifting Particles) ──
    ambientParticles.forEach(p => {
        let py = p.y * h;
        let px = p.x * w;
        
        ctx.fillStyle = p.color;
        ctx.globalAlpha = 0.6;
        ctx.beginPath();
        ctx.arc(px, py, p.size, 0, Math.PI * 2);
        ctx.fill();
    });
    ctx.globalAlpha = 1.0;
    

    // ── Draw Energy Tower Walls ───────────────────────
    const wallColor = '#120024'; // dark purple solid body
    ctx.fillStyle = wallColor; 
    
    // Left Wall Body
    ctx.fillRect(0, 0, WALL_WIDTH, h);
    // Right Wall Body
    ctx.fillRect(w - WALL_WIDTH, 0, WALL_WIDTH, h);

    // Wall texture/paneling (subtle grid/lines)
    ctx.strokeStyle = 'rgba(80, 0, 150, 0.2)';
    ctx.lineWidth = 1;
    for (let i = 0; i < h; i += 40) {
        let yShift = (i + scrollOffset) % h;
        ctx.strokeRect(0, yShift, WALL_WIDTH, 20);
        ctx.strokeRect(w - WALL_WIDTH, yShift, WALL_WIDTH, 20);
    }

    // Glowing inner edge trim (Hot Pink / Magenta)
    ctx.strokeStyle = '#ff00aa';
    ctx.lineWidth = 4;

    ctx.beginPath();
    ctx.moveTo(WALL_WIDTH, 0);
    ctx.lineTo(WALL_WIDTH, h);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(w - WALL_WIDTH, 0);
    ctx.lineTo(w - WALL_WIDTH, h);
    ctx.stroke();
    
    // Add white hot edge highlight

    ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(WALL_WIDTH, 0);
    ctx.lineTo(WALL_WIDTH, h);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(w - WALL_WIDTH, 0);
    ctx.lineTo(w - WALL_WIDTH, h);
    ctx.stroke();
    

    // ── Draw Multi-layered Crystal Obstacles ────────
    obstacles.forEach(ob => {
        if (ob.passed) {
            ctx.globalAlpha = Math.max(0, 1 - (ob.y - player.y) / 300);
        }
        
        ctx.save();
        
        if (ob.type === 'spiral' || ob.type === 'flipper' || ob.type === 'wormhole') {
            const obX = ob.lane === 0 ? WALL_WIDTH + ob.radius + 15 : w - WALL_WIDTH - ob.radius - 15;
            ctx.translate(obX, ob.y);
            ctx.rotate(ob.rotation);
            
            if (ob.type === 'wormhole') {
                // Neon blue spiral diamond
                ctx.shadowBlur = 25;
                ctx.shadowColor = '#00ffff';
                ctx.strokeStyle = '#00ffff';
                ctx.lineWidth = 3;
                
                // Outer diamond
                ctx.fillStyle = 'rgba(0, 255, 255, 0.2)';
                ctx.beginPath();
                ctx.moveTo(0, -ob.radius);
                ctx.lineTo(ob.radius, 0);
                ctx.lineTo(0, ob.radius);
                ctx.lineTo(-ob.radius, 0);
                ctx.closePath();
                ctx.fill();
                ctx.stroke();

                // Inner spiral
                ctx.beginPath();
                for (let i = 0; i < Math.PI * 6; i += 0.2) {
                    const r = (i / (Math.PI * 6)) * (ob.radius * 0.8);
                    const sx = Math.cos(-i) * r;
                    const sy = Math.sin(-i) * r;
                    if (i === 0) ctx.moveTo(sx, sy);
                    else ctx.lineTo(sx, sy);
                }
                ctx.stroke();
                
                // Inner core
                ctx.fillStyle = '#ffffff';
                ctx.shadowBlur = 10;
                ctx.shadowColor = '#ffffff';
                ctx.beginPath();
                ctx.arc(0, 0, ob.radius * 0.2, 0, Math.PI * 2);
                ctx.fill();
            } else if (ob.type === 'spiral') {
                // Draw a spinning red spiral
                ctx.shadowBlur = 20;
                ctx.shadowColor = '#ff0055';
                ctx.strokeStyle = '#ff0055';
                ctx.lineWidth = 4;
                
                ctx.beginPath();
                // Draw a spiral using polar coordinates
                for (let i = 0; i < Math.PI * 6; i += 0.2) { // 3 full coils
                    const r = (i / (Math.PI * 6)) * ob.radius;
                    const sx = Math.cos(i) * r;
                    const sy = Math.sin(i) * r;
                    if (i === 0) ctx.moveTo(sx, sy);
                    else ctx.lineTo(sx, sy);
                }
                ctx.stroke();
                
                // Draw a secondary inverted coil for a cooler effect
                ctx.beginPath();
                for (let i = 0; i < Math.PI * 6; i += 0.2) {
                    const r = (i / (Math.PI * 6)) * ob.radius;
                    const sx = Math.cos(i + Math.PI) * r;
                    const sy = Math.sin(i + Math.PI) * r;
                    if (i === 0) ctx.moveTo(sx, sy);
                    else ctx.lineTo(sx, sy);
                }
                ctx.stroke();
                
                // Inner core
                ctx.fillStyle = '#ffffff';
                ctx.shadowBlur = 10;
                ctx.shadowColor = '#ffffff';
                ctx.beginPath();
                ctx.arc(0, 0, ob.radius * 0.25, 0, Math.PI * 2);
                ctx.fill();
            } else {
                // Draw a green diamond (flipper)
                ctx.beginPath();
                ctx.moveTo(0, -ob.radius);
                ctx.lineTo(ob.radius, 0);
                ctx.lineTo(0, ob.radius);
                ctx.lineTo(-ob.radius, 0);
                ctx.closePath();
                ctx.strokeStyle = '#00ff55';
                ctx.lineWidth = 3;
                ctx.stroke();
                
                // Inner diamond
                ctx.beginPath();
                ctx.moveTo(0, -ob.radius * 0.5);
                ctx.lineTo(ob.radius * 0.5, 0);
                ctx.lineTo(0, ob.radius * 0.5);
                ctx.lineTo(-ob.radius * 0.5, 0);
                ctx.closePath();
                ctx.fillStyle = 'rgba(0, 255, 85, 0.3)';
                ctx.fill();
                
                // Outer glow
                ctx.shadowBlur = 15;
                ctx.shadowColor = '#00ff55';
            }
            
        } else {
            // Add a bright neon glow to spikes so they stand out more at high speeds
            ctx.shadowBlur = 20;
            ctx.shadowColor = 'rgba(0, 255, 255, 0.9)'; // Bright cyan glow for high contrast
            ctx.filter = 'brightness(1.5)'; // Boost the image brightness directly
            
            if (ob.lane === 0) {
                // Left wall
                ctx.translate(WALL_WIDTH, ob.y);
                // Flip so the base is on the left
                ctx.scale(-1, 1);
                ctx.drawImage(ob.variant.img, -ob.depth, 0, ob.depth, ob.height);
            } else {
                // Right wall
                ctx.translate(w - WALL_WIDTH - ob.depth, ob.y);
                ctx.drawImage(ob.variant.img, 0, 0, ob.depth, ob.height);
            }
            
            ctx.filter = 'none'; // Reset filter
        }
        ctx.restore();
        ctx.globalAlpha = 1;
    });

    // ── Draw Player ───────────────────────────
    if (isPlaying || freezeTime > 0) {
        const px = player.visualX;
        const py = player.visualY || player.y;

        // Trail (Drawn behind the player)
        if (player.history) {
            ctx.shadowBlur = 20;
            ctx.shadowColor = selectedOrbColor;
            for (let i = 0; i < player.history.length; i++) {
                const pt = player.history[i];
                const ratio = i / player.history.length;
                ctx.globalAlpha = ratio * 0.6; // Fades out towards the tail
                ctx.fillStyle = selectedOrbColor;
                ctx.beginPath();
                ctx.arc(pt.x, pt.y, PLAYER_RADIUS * Math.max(0.2, (0.4 + 0.6 * ratio)), 0, Math.PI * 2);
                ctx.fill();
            }
        }
        ctx.globalAlpha = 1.0;

        ctx.shadowBlur = selectedOrbId === 0 ? 15 : (selectedOrbId >= 10 ? 80 : 45);
        ctx.shadowColor = selectedOrbColor;

        if (selectedOrbId === 0) {
            // Draw procedural default neon ring
            ctx.fillStyle = selectedOrbColor;
            ctx.beginPath();
            ctx.arc(px, py, PLAYER_RADIUS, 0, Math.PI * 2);
            ctx.fill();

            // Inner bright core
            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.arc(px, py, PLAYER_RADIUS * 0.45, 0, Math.PI * 2);
            ctx.fill();
            
            // Center diamond
            ctx.fillStyle = '#ccffff';
            ctx.beginPath();
            ctx.moveTo(px, py - PLAYER_RADIUS * 0.8);
            ctx.lineTo(px + PLAYER_RADIUS * 0.6, py);
            ctx.lineTo(px, py + PLAYER_RADIUS * 0.8);
            ctx.lineTo(px - PLAYER_RADIUS * 0.6, py);
            ctx.closePath();
            ctx.fill();
        } else {
            // Draw custom orb
            const playerSize = PLAYER_RADIUS * 2 * (selectedOrbId >= 10 ? 2.4 : 1.8); 
            if (customOrbImage && customOrbImage.complete) {
                const aspect = customOrbImage.width / customOrbImage.height;
                let drawW = playerSize;
                let drawH = playerSize;
                if (aspect > 1) {
                    drawH = playerSize / aspect;
                } else if (aspect < 1) {
                    drawW = playerSize * aspect;
                }
                ctx.drawImage(
                    customOrbImage,
                    px - drawW / 2,
                    py - drawH / 2,
                    drawW,
                    drawH
                );
            }
        }
        ctx.shadowBlur = 0; // reset
    }

    
    

    // ── Draw Particles ────────────────────────────
    particles.forEach(p => {
        ctx.globalAlpha = p.life !== undefined ? Math.max(0, Math.min(1, p.life)) : 1;
        
        if (p.isShatter) {
            ctx.save();
            ctx.translate(p.x, p.y);
            ctx.rotate(p.angle || 0);
            ctx.fillStyle = p.color;
            ctx.shadowBlur = 15;
            ctx.shadowColor = p.color;
            ctx.beginPath();
            ctx.moveTo(0, -p.size);
            ctx.lineTo(p.size * 0.8, p.size);
            ctx.lineTo(-p.size * 0.8, p.size);
            ctx.closePath();
            ctx.fill();
            ctx.restore();
        } else if (p.isEmber) {
            ctx.save();
            ctx.fillStyle = '#ffffff';
            ctx.shadowBlur = 10;
            ctx.shadowColor = '#ffffff';
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        } else {
            ctx.fillStyle = p.color || '#ff00ff';
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
        }
    });
    ctx.globalAlpha = 1.0;

    // ── Bottom Fog / Energy Mist ───────────────────────
    const fogGrad = ctx.createLinearGradient(0, h - 150, 0, h);
    fogGrad.addColorStop(0, 'rgba(255, 0, 255, 0)');
    fogGrad.addColorStop(1, 'rgba(200, 0, 255, 0.4)');
    ctx.fillStyle = fogGrad;
    ctx.fillRect(0, h - 150, w, 150);

    // ── HUD ───────────────────────────────────────────
    drawHUD(w, h);

    ctx.restore();
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
    
    // Counter-rotate the entire HUD so it stays upright when the canvas spins
    ctx.translate(cx, h / 2);
    ctx.rotate(-angleDeg * (Math.PI / 180));
    ctx.translate(-cx, -h / 2);
    
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    // Outer glow layer
    ctx.font = 'bold 72px "Courier New", monospace';
    ctx.shadowBlur = 10;
    ctx.shadowColor = 'rgba(0,255,255,0.5)';
    ctx.fillStyle = 'rgba(0,255,255,0.12)';
    ctx.fillText(scoreStr, cx, 60);

    // Main score text
    ctx.shadowBlur = 5;
    ctx.shadowColor = '#ff00ff';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(scoreStr, cx, 60);
    

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

    

    // ── Multiplier badge ──────────────
    if (mult > 1) {
        const multStr = `x${mult}`;
        ctx.font = 'bold 28px "Courier New", monospace';
        
        ctx.shadowColor = '#ff00ff';

        // Pulse alpha with time
        const pulse = 0.7 + 0.3 * Math.sin(performance.now() * 0.008);
        ctx.fillStyle = `rgba(0,255,255,${pulse})`;
        ctx.fillText(multStr, cx, 120);
        
    }

    // ── "COMBO" label left wall ───────
    if (combo > 0) {
        ctx.font = '12px "Courier New", monospace';
        ctx.fillStyle = 'rgba(255,255,255,0.35)';
        ctx.textAlign = 'left';
        ctx.fillText('COMBO', WALL_WIDTH + 8, 30);
        ctx.font = 'bold 22px "Courier New", monospace';
        ctx.fillStyle = '#ff00ff';
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

window.addEventListener('beforeunload', () => { bgMusic.pause(); });
