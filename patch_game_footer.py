import re

with open('game.html', 'r') as f:
    game_html = f.read()

footer = """    </div>
    
    <!-- Site Footer -->
    <footer class="site-footer" style="margin-top: auto; width: 100%; max-width: 800px;">
        <a href="index.html">Home</a>
        <a href="privacy.html">Privacy Policy</a>
        <a href="terms.html">Terms of Service</a>
        <a href="mailto:contact@walldash.com">Contact Us</a>
    </footer>

    <script src="game.js?v=18"></script>"""

game_html = game_html.replace('    </div>\n    \n    <script src="game.js?v=18"></script>', footer)

with open('game.html', 'w') as f:
    f.write(game_html)
