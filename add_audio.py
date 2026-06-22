with open('game.js', 'r') as f:
    js = f.read()

audio_code = """
// --- Audio System ---
const playlist = [
    'monume-synthwave-retro-80s-498055.mp3',
    'monume-cyberpunk-547930.mp3',
    'delosound-inspiring-motivation-synthwave-398285.mp3',
    'the_mountain-electronic-retrowave-132335.mp3'
];

let shuffledPlaylist = [];
let currentTrackIndex = 0;
let bgMusic = new Audio();
bgMusic.volume = 0.5;

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function playNextTrack() {
    if (currentTrackIndex >= shuffledPlaylist.length) {
        // Reshuffle when we reach the end
        shuffledPlaylist = shuffleArray([...playlist]);
        currentTrackIndex = 0;
    }
    
    bgMusic.src = shuffledPlaylist[currentTrackIndex];
    bgMusic.play().catch(e => console.log("Audio play blocked by browser:", e));
    currentTrackIndex++;
}

bgMusic.addEventListener('ended', () => {
    // 5 seconds delay before next song
    setTimeout(playNextTrack, 5000);
});

let audioStarted = false;
function initAudio() {
    if (!audioStarted) {
        audioStarted = true;
        shuffledPlaylist = shuffleArray([...playlist]);
        playNextTrack();
    }
}

// Add interaction listener to start audio as soon as possible due to browser policies
window.addEventListener('click', initAudio, { once: true });
window.addEventListener('keydown', initAudio, { once: true });
window.addEventListener('touchstart', initAudio, { once: true });
"""

if '// --- Audio System ---' not in js:
    js = audio_code + '\n' + js
    with open('game.js', 'w') as f:
        f.write(js)
    print("Audio system added.")
else:
    print("Audio system already exists.")

