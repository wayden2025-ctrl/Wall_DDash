import os
import re

privacy_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policy - Wall Dash</title>
    <link rel="stylesheet" href="style.css?v=2">
</head>
<body style="display: flex; flex-direction: column; align-items: center; padding: 40px 20px; font-family: 'Courier New', Courier, monospace; color: #a0a0b0;">
    <div style="max-width: 800px; width: 100%; text-align: left;">
        <h1 style="color: #00ffff; text-shadow: 0 0 10px rgba(0,255,255,0.5);">Privacy Policy</h1>
        <p>Last updated: June 2026</p>
        
        <h2 style="color: #ff00ff; margin-top: 20px;">1. Introduction</h2>
        <p>Welcome to Wall Dash. We respect your privacy and are committed to protecting your personal data. This privacy policy will inform you as to how we look after your personal data when you visit our website.</p>
        
        <h2 style="color: #ff00ff; margin-top: 20px;">2. Advertising and Cookies</h2>
        <p>We use third-party advertising companies, including Google, to serve ads when you visit our website. These companies may use information (not including your name, address, email address, or telephone number) about your visits to this and other websites in order to provide advertisements about goods and services of interest to you.</p>
        <ul>
            <li>Third party vendors, including Google, use cookies to serve ads based on a user's prior visits to your website or other websites.</li>
            <li>Google's use of advertising cookies enables it and its partners to serve ads to your users based on their visit to your sites and/or other sites on the Internet.</li>
            <li>Users may opt out of personalized advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank" style="color: #00ffff;">Ads Settings</a>.</li>
        </ul>
        
        <h2 style="color: #ff00ff; margin-top: 20px;">3. Analytics</h2>
        <p>We use analytics tools to measure website traffic and improve user experience. These tools may collect anonymous usage data.</p>
        
        <h2 style="color: #ff00ff; margin-top: 20px;">4. Contact Us</h2>
        <p>If you have any questions about this Privacy Policy, you can contact us at: contact@walldash.com</p>
        
        <div style="margin-top: 40px;">
            <a href="index.html" style="color: #00ffff; text-decoration: none;">&larr; Back to Home</a>
        </div>
    </div>
</body>
</html>"""

terms_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terms of Service - Wall Dash</title>
    <link rel="stylesheet" href="style.css?v=2">
</head>
<body style="display: flex; flex-direction: column; align-items: center; padding: 40px 20px; font-family: 'Courier New', Courier, monospace; color: #a0a0b0;">
    <div style="max-width: 800px; width: 100%; text-align: left;">
        <h1 style="color: #00ffff; text-shadow: 0 0 10px rgba(0,255,255,0.5);">Terms of Service</h1>
        <p>Last updated: June 2026</p>
        
        <h2 style="color: #ff00ff; margin-top: 20px;">1. Acceptance of Terms</h2>
        <p>By accessing and playing Wall Dash, you accept and agree to be bound by the terms and provision of this agreement.</p>
        
        <h2 style="color: #ff00ff; margin-top: 20px;">2. Use License</h2>
        <p>Permission is granted to temporarily play the game on Wall Dash's website for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title.</p>
        
        <h2 style="color: #ff00ff; margin-top: 20px;">3. Disclaimer</h2>
        <p>The materials on Wall Dash's website are provided on an 'as is' basis. Wall Dash makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including, without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.</p>
        
        <h2 style="color: #ff00ff; margin-top: 20px;">4. Limitations</h2>
        <p>In no event shall Wall Dash or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on Wall Dash's website.</p>
        
        <div style="margin-top: 40px;">
            <a href="index.html" style="color: #00ffff; text-decoration: none;">&larr; Back to Home</a>
        </div>
    </div>
</body>
</html>"""

with open('privacy.html', 'w') as f:
    f.write(privacy_content)

with open('terms.html', 'w') as f:
    f.write(terms_content)

# Update index.html
with open('index.html', 'r') as f:
    index_html = f.read()

# Expanded content for index
expanded_content = """<!-- Publisher Content Section for AdSense Policy Compliance -->
            <div id="publisher-content" style="max-width: 800px; margin: 40px auto; padding: 20px; font-family: 'Courier New', Courier, monospace; color: #a0a0b0; line-height: 1.6; text-align: left;">
                <h2 style="color: #00ffff; margin-bottom: 15px; font-size: 24px;">About Wall Dash: The Cyber Void</h2>
                <p style="margin-bottom: 20px; font-size: 15px;">
                    <strong>Wall Dash</strong> is a high-octane, reflex-driven endless runner set deep within the neon-lit confines of the Cyber Void. As a rogue data packet, your objective is to survive for as long as possible while the system attempts to purge you using an array of deadly, crystallized security spikes. The longer you survive, the faster the system purges, demanding lightning-fast reflexes and flawless timing.
                </p>

                <h3 style="color: #ff00ff; margin-bottom: 10px; font-size: 20px;">How to Play & Master the Game</h3>
                <p style="margin-bottom: 10px; font-size: 15px;">
                    The controls are beautifully simple but incredibly hard to master. You can tap the screen on mobile devices, click your mouse, or press the Spacebar on your keyboard to instantly switch from the left wall to the right wall.
                </p>
                <p style="margin-bottom: 20px; font-size: 15px;">
                    <strong>Pro Tip:</strong> Timing is everything. While you can spam the dash button to stay safe, timing your dashes at the very last second before impact will grant you a "PERFECT!" dodge rating. Chaining these perfect dodges together will dramatically increase your score multiplier, allowing you to dominate the leaderboards!
                </p>

                <h3 style="color: #00ffff; margin-bottom: 10px; font-size: 20px;">Key Features</h3>
                <ul style="margin-left: 20px; margin-bottom: 20px; font-size: 15px;">
                    <li style="margin-bottom: 8px;"><strong>Hyper-Responsive Controls:</strong> Enjoy zero-latency lane switching, perfectly optimized for both high-refresh-rate desktop monitors and mobile touchscreens.</li>
                    <li style="margin-bottom: 8px;"><strong>Premium Cyberpunk Aesthetics:</strong> Immerse yourself in glowing neon graphics, dynamic particle burst effects upon near-misses, and a mesmerizing Matrix-style code rain background.</li>
                    <li style="margin-bottom: 8px;"><strong>Dynamic Difficulty Scaling:</strong> There are no levels—only an infinite vertical tunnel that continuously accelerates. The speed and intensity of the obstacle generation automatically scale up the longer you manage to stay alive.</li>
                    <li style="margin-bottom: 8px;"><strong>Cross-Platform Play:</strong> Designed entirely in HTML5 and pure JavaScript, Wall Dash runs flawlessly in your browser without any downloads required.</li>
                </ul>
            </div>
            
            <!-- Site Footer -->
            <footer class="site-footer">
                <a href="index.html">Home</a>
                <a href="privacy.html">Privacy Policy</a>
                <a href="terms.html">Terms of Service</a>
                <a href="mailto:contact@walldash.com">Contact Us</a>
                <p>&copy; 2026 Wall Dash. All rights reserved.</p>
            </footer>"""

index_html = re.sub(r'<!-- Publisher Content Section for AdSense Policy Compliance -->.*?</div>', expanded_content, index_html, flags=re.DOTALL)

# Add Cookie Banner
cookie_banner = """    <div id="cookie-banner" class="cookie-banner">
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

index_html = index_html.replace('</body>', cookie_banner)

with open('index.html', 'w') as f:
    f.write(index_html)

print("Legal pages created and index updated.")
