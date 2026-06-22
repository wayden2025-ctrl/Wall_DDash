import re

for filepath in ['game.html', 'index.html']:
    with open(filepath, 'r') as f:
        html = f.read()

    # 1. Strip the harmful inline 'display: flex' that breaks mobile, and enforce strict flex-basis 0 for perfect balance
    html = re.sub(
        r'class="ad-space-desktop left-ad" style="[^"]*"', 
        r'class="ad-space-desktop left-ad" style="flex: 1 1 0; min-width: 0; max-width: calc(50vw - 300px);"', 
        html
    )
    html = re.sub(
        r'class="ad-space-desktop right-ad" style="[^"]*"', 
        r'class="ad-space-desktop right-ad" style="flex: 1 1 0; min-width: 0; max-width: calc(50vw - 300px);"', 
        html
    )

    # 2. Add justify-content: center to the main layout to keep it centered when sidebars are hidden
    html = html.replace(
        'class="desktop-main-layout" style="display: flex; flex: 1; width: 100%; height: 100%; overflow: hidden;"',
        'class="desktop-main-layout" style="display: flex; flex: 1; width: 100%; height: 100%; overflow: hidden; justify-content: center;"'
    )
    html = html.replace(
        'class="desktop-main-layout" style="display: flex; flex: 1; width: 100%;"',
        'class="desktop-main-layout" style="display: flex; flex: 1; width: 100%; justify-content: center;"'
    )

    # 3. Ensure the footer centers correctly and doesn't get pushed to the left
    html = re.sub(
        r'<footer class="site-footer" style="[^"]*">',
        '<footer class="site-footer" style="margin-top: auto; width: 100%; max-width: 800px; margin-left: auto; margin-right: auto; text-align: center;">',
        html
    )
    # Just in case index.html doesn't have a style attribute on footer
    html = html.replace('<footer class="site-footer">', '<footer class="site-footer" style="margin-top: auto; width: 100%; max-width: 800px; margin-left: auto; margin-right: auto; text-align: center;">')

    # 4. In game.html, make sure the center column is allowed to be flexible but bounded
    if 'game.html' in filepath:
        html = html.replace(
            '<div style="flex: 0 1 600px; max-width: 600px; width: 100%; height: 100%; position: relative;">',
            '<div style="flex: 1 1 100%; max-width: 600px; width: 100%; height: 100%; position: relative;">'
        )

    # 5. Fix logo scaling so it doesn't break out of the container
    html = html.replace(
        'max-width: 90%; max-height: 250px;',
        'max-width: 100%; height: auto; max-height: 250px; object-fit: contain;'
    )

    with open(filepath, 'w') as f:
        f.write(html)

print("Layout strictly balanced.")
