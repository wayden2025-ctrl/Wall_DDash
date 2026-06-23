with open('index.html', 'r') as f:
    index_lines = f.readlines()

with open('game.html', 'r') as f:
    game_lines = f.readlines()

# Extract lines 125 to 185 (0-indexed) from index.html
store_modal_lines = index_lines[125:186]

# Find the start and end of the store modal in game.html
start_idx = -1
end_idx = -1
for i, line in enumerate(game_lines):
    if "<!-- Store Modal -->" in line:
        start_idx = i
    if start_idx != -1 and line.strip() == "</div>" and "    </div>" in line:
        if i > start_idx + 20: # Make sure it's the closing div of the modal
            end_idx = i
            break

if start_idx != -1 and end_idx != -1:
    new_game_lines = game_lines[:start_idx] + store_modal_lines + game_lines[end_idx+1:]
    with open('game.html', 'w') as f:
        f.writelines(new_game_lines)
    print("Fixed store modal in game.html")
else:
    print("Could not find store modal in game.html")
