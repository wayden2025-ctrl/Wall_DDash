import re

# Patch index.html
with open('index.html', 'r') as f:
    index_html = f.read()

# Make sidebars expand
index_html = index_html.replace('style="flex: 0 0 320px;"', 'style="flex: 1 1 auto; min-width: 160px; display: flex; flex-direction: column; justify-content: center;"')
# Keep center container fixed max width
index_html = index_html.replace('style="flex: 1 1 auto; width: 100%; display: flex;', 'style="flex: 0 1 800px; max-width: 800px; width: 100%; display: flex;')

with open('index.html', 'w') as f:
    f.write(index_html)


# Patch game.html
with open('game.html', 'r') as f:
    game_html = f.read()

# Add body flex
game_html = game_html.replace('body style="width: 100vw; height: 100vh; overflow: hidden; margin: 0; padding: 0; background-color: #050508;"', 'body style="width: 100vw; height: 100vh; overflow: hidden; margin: 0; padding: 0; background-color: #050508; display: flex; flex-direction: column;"')

# Add AdSense auto ad script to game.html head if not present
if 'adsbygoogle.js' not in game_html:
    head_insertion = """    <script defer src="/_vercel/insights/script.js"></script>
    <!-- Google AdSense Auto Ads -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6859171401389344" crossorigin="anonymous"></script>"""
    game_html = game_html.replace('    <script defer src="/_vercel/insights/script.js"></script>', head_insertion)

# Wrap game-container
game_container_start = '<div id="game-container"'

layout_wrapper = """    <div class="desktop-main-layout" style="display: flex; flex: 1; width: 100%; height: 100%; overflow: hidden;">
        <!-- Left Desktop Ads -->
        <div class="ad-space-desktop left-ad" style="flex: 1 1 auto; min-width: 160px; display: flex; flex-direction: column; justify-content: center;">
            <ins class="adsbygoogle"
                 style="display:block"
                 data-ad-client="ca-pub-6859171401389344"
                 data-ad-slot="5414697527"
                 data-ad-format="auto"
                 data-full-width-responsive="true"></ins>
            <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
        </div>
        
        <div style="flex: 0 1 600px; max-width: 600px; width: 100%; height: 100%; position: relative;">
            <div id="game-container\""""

game_html = game_html.replace(game_container_start, layout_wrapper)

# Close the wrapper before the footer
footer_start = '    <!-- Site Footer -->'
layout_closer = """            </div> <!-- End inner wrapper -->
        </div>
        
        <!-- Right Desktop Ads -->
        <div class="ad-space-desktop right-ad" style="flex: 1 1 auto; min-width: 160px; display: flex; flex-direction: column; justify-content: center;"></div>
    </div>

    <!-- Site Footer -->"""
game_html = game_html.replace(footer_start, layout_closer)

with open('game.html', 'w') as f:
    f.write(game_html)

print("Layout patched.")
