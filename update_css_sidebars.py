with open('style.css', 'r') as f:
    css = f.read()

sidebar_css = """
/* Desktop Ad Sidebars */
.ad-space-desktop {
    display: none;
}

@media (min-width: 1000px) {
    .ad-space-desktop {
        display: block;
        overflow: hidden;
    }
}
"""

if '.ad-space-desktop' not in css:
    css += sidebar_css
    with open('style.css', 'w') as f:
        f.write(css)
    print("Added CSS.")
else:
    print("CSS already exists.")
