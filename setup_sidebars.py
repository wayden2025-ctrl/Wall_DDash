import re

# 1. Process game.html
with open('game.html', 'r') as f:
    game_html = f.read()

game_html = game_html.replace(
    '<body style="width: 100vw; height: 100vh; overflow: hidden; margin: 0; padding: 0; background-color: #050508;">',
    '<body style="width: 100vw; height: 100vh; overflow: hidden; margin: 0; padding: 0; background-color: #050508; display: flex; flex-direction: column;">\n    <div class="desktop-main-layout" style="display: flex; flex: 1; width: 100%; height: 100%; overflow: hidden; justify-content: center;">\n        <div class="ad-space-desktop left-ad" style="flex: 1 1 0; min-width: 0; max-width: calc(50vw - 300px);">\n            <ins class="adsbygoogle"\n                 style="display:block"\n                 data-ad-client="ca-pub-6859171401389344"\n                 data-ad-slot="5414697527"\n                 data-ad-format="auto"\n                 data-full-width-responsive="true"></ins>\n            <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>\n        </div>\n        \n        <div style="flex: 1 1 100%; max-width: 600px; width: 100%; height: 100%; position: relative;">'
)

game_html = game_html.replace(
    '    </div>\n    \n    <!-- Site Footer -->',
    '    </div>\n        </div>\n        <div class="ad-space-desktop right-ad" style="flex: 1 1 0; min-width: 0; max-width: calc(50vw - 300px);"></div>\n    </div>\n    \n    <!-- Site Footer -->'
)

game_html = game_html.replace(
    '<footer class="site-footer" style="margin-top: auto; width: 100%; max-width: 800px;">',
    '<footer class="site-footer" style="margin-top: auto; width: 100%; max-width: 800px; margin-left: auto; margin-right: auto; text-align: center;">'
)

with open('game.html', 'w') as f:
    f.write(game_html)


# 2. Process index.html
with open('index.html', 'r') as f:
    index_html = f.read()

index_html = index_html.replace(
    '<body style="display: flex; flex-direction: column; width: 100vw; min-height: 100vh; margin: 0; padding: 0; background-color: #050508; overflow-x: hidden;">',
    '<body style="display: flex; flex-direction: column; width: 100vw; min-height: 100vh; margin: 0; padding: 0; background-color: #050508; overflow-x: hidden;">\n    <div class="desktop-main-layout" style="display: flex; flex: 1; width: 100%; justify-content: center;">\n        <div class="ad-space-desktop left-ad" style="flex: 1 1 0; min-width: 0; max-width: calc(50vw - 300px);">\n            <ins class="adsbygoogle"\n                 style="display:block"\n                 data-ad-client="ca-pub-6859171401389344"\n                 data-ad-slot="5414697527"\n                 data-ad-format="auto"\n                 data-full-width-responsive="true"></ins>\n            <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>\n        </div>\n        \n        <div style="flex: 1 1 100%; max-width: 600px; width: 100%;">'
)

index_html = index_html.replace(
    '    <!-- Site Footer -->',
    '        </div>\n        <div class="ad-space-desktop right-ad" style="flex: 1 1 0; min-width: 0; max-width: calc(50vw - 300px);"></div>\n    </div>\n    \n    <!-- Site Footer -->'
)

index_html = index_html.replace(
    '<footer class="site-footer">',
    '<footer class="site-footer" style="margin-top: auto; width: 100%; max-width: 800px; margin-left: auto; margin-right: auto; text-align: center;">'
)

with open('index.html', 'w') as f:
    f.write(index_html)

print("Sidebars added correctly.")
