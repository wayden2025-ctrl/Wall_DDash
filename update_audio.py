with open('game.js', 'r') as f:
    js = f.read()

# We need to extract the existing audio system block and replace it
import re

audio_pattern = r'// --- Audio System ---.*?window\.addEventListener\(\'touchstart\', initAudio, { once: true }\);'
new_audio_code = """// --- Audio System ---
const playlist = [
    'monume-synthwave-retro-80s-498055.m4a',
    'monume-cyberpunk-547930.m4a',
    'delosound-inspiring-motivation-synthwave-398285.m4a',
    'the_mountain-electronic-retrowave-132335.m4a'
];

let bgMusic = new Audio();
bgMusic.volume = 0.5;

function playNextTrack() {
    // Load the current track index from local storage (defaults to 0)
    let trackIndex = parseInt(localStorage.getItem('wallDashMusicIndex') || '0', 10);
    
    // Failsafe if index is out of bounds
    if (trackIndex >= playlist.length || isNaN(trackIndex)) {
        trackIndex = 0;
    }
    
    bgMusic.src = playlist[trackIndex];
    bgMusic.play().catch(e => console.log("Audio play blocked by browser:", e));
    
    // Save the next track index for when the song finishes OR the user restarts the game
    let nextIndex = (trackIndex + 1) % playlist.length;
    localStorage.setItem('wallDashMusicIndex', nextIndex);
}

bgMusic.addEventListener('ended', () => {
    // 5 seconds delay before next song
    setTimeout(playNextTrack, 5000);
});

let audioStarted = false;
function initAudio() {
    if (!audioStarted) {
        audioStarted = true;
        playNextTrack();
    }
}

// Add interaction listener to start audio as soon as possible due to browser policies
window.addEventListener('click', initAudio, { once: true });
window.addEventListener('keydown', initAudio, { once: true });
window.addEventListener('touchstart', initAudio, { once: true });"""

if re.search(audio_pattern, js, re.DOTALL):
    js = re.sub(audio_pattern, new_audio_code, js, flags=re.DOTALL)
    with open('game.js', 'w') as f:
        f.write(js)
    print("Audio system updated for persistent cycling.")
else:
    print("Could not find audio block to replace!")

