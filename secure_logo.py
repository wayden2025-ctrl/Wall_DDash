for filepath in ['game.html', 'index.html']:
    with open(filepath, 'r') as f:
        html = f.read()

    html = html.replace(
        'max-width: 90%; max-height: 250px;',
        'max-width: 100%; height: auto; max-height: 250px; object-fit: contain;'
    )

    with open(filepath, 'w') as f:
        f.write(html)
print("Secured logo sizing.")
