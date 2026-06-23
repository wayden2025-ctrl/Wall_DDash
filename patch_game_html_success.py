import re

with open('game.html', 'r') as f:
    html = f.read()

handler = """        document.addEventListener("DOMContentLoaded", function() {
            if (!localStorage.getItem('cookiesAccepted')) {
                document.getElementById('cookie-banner').style.display = 'flex';
            }
            document.getElementById('accept-cookies').addEventListener('click', function() {
                localStorage.setItem('cookiesAccepted', 'true');
                document.getElementById('cookie-banner').style.display = 'none';
            });
            
            // Handle Stripe redirects
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('success') === 'true') {
                localStorage.setItem('premiumBundleUnlocked', 'true');
                document.getElementById('store-modal').style.display = 'flex';
                const cm = document.getElementById('checkout-container');
                if(cm) cm.style.display = 'none';
                const sm = document.getElementById('success-msg');
                if(sm) sm.style.display = 'block';
                window.history.replaceState({}, document.title, window.location.pathname);
            }
            if (urlParams.get('revive_success') === 'true') {
                let currentRevives = parseInt(localStorage.getItem('revivesLeft')) || 0;
                localStorage.setItem('revivesLeft', (currentRevives + 10).toString());
                alert("Purchase Successful! 10 Revives have been added to your account.");
                window.history.replaceState({}, document.title, window.location.pathname);
            }
        });"""

html = re.sub(r'document\.addEventListener\("DOMContentLoaded", function\(\) \{\s+if \(!localStorage\.getItem\(\'cookiesAccepted\'\)\) \{\s+document\.getElementById\(\'cookie-banner\'\)\.style\.display = \'flex\';\s+\}\s+document\.getElementById\(\'accept-cookies\'\)\.addEventListener\(\'click\', function\(\) \{\s+localStorage\.setItem\(\'cookiesAccepted\', \'true\'\);\s+document\.getElementById\(\'cookie-banner\'\)\.style\.display = \'none\';\s+\}\);\s+\}\);', handler, html)

with open('game.html', 'w') as f:
    f.write(html)
print("game.html patched for success redirects.")
