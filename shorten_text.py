import re

with open('index.html', 'r') as f:
    html = f.read()

# Pattern to find the publisher content div and everything inside it
pattern = r'(<div id="publisher-content" style="max-width: 800px; margin: 40px auto; padding: 20px; font-family: \'Courier New\', Courier, monospace; color: #a0a0b0; line-height: 1\.6; text-align: left;">\s*<h2 style="color: #00ffff; margin-bottom: 15px; font-size: 24px;">About Wall Dash: The Cyber Void</h2>)(.*?)(</div>\s*</div>)'

new_content = """<div id="publisher-content" style="max-width: 800px; margin: 40px auto; padding: 20px; font-family: 'Courier New', Courier, monospace; color: #a0a0b0; line-height: 1.6; text-align: left;">
                <h2 style="color: #00ffff; margin-bottom: 15px; font-size: 24px;">About Wall Dash</h2>
                <p style="margin-bottom: 20px; font-size: 15px;">
                    <strong>Wall Dash</strong> is a fast-paced HTML5 arcade game where you must survive the neon Cyber Void by dodging deadly security spikes. It features dynamic difficulty scaling, meaning the game accelerates the longer you stay alive.
                </p>
                <h3 style="color: #ff00ff; margin-bottom: 10px; font-size: 20px;">How to Play</h3>
                <ul style="margin-left: 20px; margin-bottom: 20px; font-size: 15px;">
                    <li style="margin-bottom: 8px;"><strong>Controls:</strong> Tap the screen, click your mouse, or press Spacebar to instantly dash between walls.</li>
                    <li style="margin-bottom: 8px;"><strong>Scoring:</strong> Dodge spikes at the very last second to earn a "PERFECT" rating and boost your score multiplier.</li>
                    <li style="margin-bottom: 8px;"><strong>Cross-Platform:</strong> Play instantly in any web browser without downloads.</li>
                </ul>
            </div>
            
                </div>"""

# I will just replace the whole publisher-content div
html = re.sub(r'<div id="publisher-content".*?</ul>\s*</div>', 
              """<div id="publisher-content" style="max-width: 800px; margin: 40px auto; padding: 20px; font-family: 'Courier New', Courier, monospace; color: #a0a0b0; line-height: 1.6; text-align: left;">
                <h2 style="color: #00ffff; margin-bottom: 15px; font-size: 24px;">About Wall Dash</h2>
                <p style="margin-bottom: 20px; font-size: 15px;">
                    <strong>Wall Dash</strong> is a fast-paced HTML5 arcade game where you must survive the neon Cyber Void by dodging deadly security spikes. It features dynamic difficulty scaling, meaning the game accelerates the longer you stay alive.
                </p>
                <h3 style="color: #ff00ff; margin-bottom: 10px; font-size: 20px;">How to Play</h3>
                <ul style="margin-left: 20px; margin-bottom: 20px; font-size: 15px;">
                    <li style="margin-bottom: 8px;"><strong>Controls:</strong> Tap the screen, click your mouse, or press Spacebar to instantly dash between walls.</li>
                    <li style="margin-bottom: 8px;"><strong>Scoring:</strong> Dodge spikes at the very last second to earn a "PERFECT" rating and boost your score multiplier.</li>
                    <li style="margin-bottom: 8px;"><strong>Cross-Platform:</strong> Play instantly in any mobile or desktop web browser.</li>
                </ul>
            </div>""", html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
print("Text shortened.")
