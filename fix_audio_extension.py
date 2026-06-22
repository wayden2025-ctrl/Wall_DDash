with open('game.js', 'r') as f:
    js = f.read()

js = js.replace('.mp3', '.m4a')

with open('game.js', 'w') as f:
    f.write(js)
print("Updated game.js to use m4a")
