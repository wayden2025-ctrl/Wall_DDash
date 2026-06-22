import re

with open('game.html', 'r') as f:
    html = f.read()

# Add the premium orbs if unlocked
injection = """    ];

    if (localStorage.getItem('premiumBundleUnlocked') === 'true') {
        orbs.push(
            { id: 10, name: 'Sapphire Core', color: '#00aaff', src: 'premium_orb_10.png', titleSrc: null },
            { id: 11, name: 'Ruby Core', color: '#ff2200', src: 'premium_orb_11.png', titleSrc: null },
            { id: 12, name: 'Emerald Core', color: '#00ff44', src: 'premium_orb_12.png', titleSrc: null },
            { id: 13, name: 'Amethyst Core', color: '#aa00ff', src: 'premium_orb_13.png', titleSrc: null },
            { id: 14, name: 'Topaz Core', color: '#ffcc00', src: 'premium_orb_14.png', titleSrc: null },
            { id: 15, name: 'Amber Core', color: '#ff7700', src: 'premium_orb_15.png', titleSrc: null },
            { id: 16, name: 'Cyan Core', color: '#00ffff', src: 'premium_orb_16.png', titleSrc: null },
            { id: 17, name: 'Magenta Core', color: '#ff00aa', src: 'premium_orb_17.png', titleSrc: null },
            { id: 18, name: 'Diamond Core', color: '#e0f7fa', src: 'premium_orb_18.png', titleSrc: null }
        );
    }"""

html = html.replace("    ];", injection, 1)

with open('game.html', 'w') as f:
    f.write(html)
print("game.html patched.")
