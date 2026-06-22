with open('game.html', 'r') as f:
    html = f.read()

cookie_banner_html = """
    <div id="cookie-banner" class="cookie-banner">
        <p>We use cookies to personalize content, provide social media features, and analyze our traffic. We also share information about your use of our site with our advertising and analytics partners. <a href="privacy.html">Learn more</a>.</p>
        <button id="accept-cookies" class="cookie-btn">Accept Cookies</button>
    </div>

    <script>
        document.addEventListener("DOMContentLoaded", function() {
            if (!localStorage.getItem('cookiesAccepted')) {
                document.getElementById('cookie-banner').style.display = 'flex';
            }
            document.getElementById('accept-cookies').addEventListener('click', function() {
                localStorage.setItem('cookiesAccepted', 'true');
                document.getElementById('cookie-banner').style.display = 'none';
            });
        });
    </script>
</body>"""

if 'id="cookie-banner"' not in html:
    html = html.replace('</body>', cookie_banner_html)
    with open('game.html', 'w') as f:
        f.write(html)
    print("Added cookie banner to game.html")
else:
    print("Banner already exists.")
