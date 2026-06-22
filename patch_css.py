with open('style.css', 'r') as f:
    css = f.read()

# Add overflow: hidden to ad spaces so they can't force the layout to break
if 'overflow: hidden;' not in css.split('.ad-space-desktop {')[1].split('}')[0]:
    css = css.replace('.ad-space-desktop {\n    display: none;', '.ad-space-desktop {\n    display: none;\n    overflow: hidden;\n    max-width: calc(50vw - 300px); /* Strictly limit width so they can never push game off center */')

with open('style.css', 'w') as f:
    f.write(css)

print("CSS patched.")
