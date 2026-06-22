import re

with open('game.js', 'r') as f:
    js = f.read()

# 1. Reverse the Y velocity (make it positive so it flies DOWN behind the player)
#    And reduce the life of the particles to make the trail shorter.
# Old: vy: -Math.random() * 300 - 150,
# New: vy: Math.random() * 300 + 150,
# Old: life: 0.4 + Math.random() * 0.4
# New: life: 0.15 + Math.random() * 0.2

js = js.replace('vy: -Math.random() * 300 - 150, // Fly backwards fast', 'vy: Math.random() * 300 + 150, // Fly DOWNWARDS behind the player')
js = js.replace('life: 0.4 + Math.random() * 0.4', 'life: 0.15 + Math.random() * 0.2')

# 2. Make the solid motion trail shorter as well (from 12 to 8 frames)
js = js.replace('if (player.history.length > 12) player.history.shift();', 'if (player.history.length > 8) player.history.shift();')

with open('game.js', 'w') as f:
    f.write(js)
print("Reversed particle direction and shortened trails!")
