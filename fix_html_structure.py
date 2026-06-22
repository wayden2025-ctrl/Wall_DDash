import re

def fix_index():
    with open('index.html', 'r') as f:
        html = f.read()

    # The issue starts around the end of publisher-content
    # Let's find where publisher-content ends
    start_str = '<!-- Publisher Content Section for AdSense Policy Compliance -->'
    idx1 = html.find(start_str)
    if idx1 == -1: return
    
    # find the end of the center column, we know publisher-content is the last thing
    # before the center column closes
    
    # We will just rewrite from the end of the </ul> inside publisher-content to the cookie-banner
    
    pattern = r'(<li style="margin-bottom: 8px;"><strong>Cross-Platform:</strong> Play instantly in any mobile or desktop web browser.</li>\s*</ul>\s*</div>).*?(<div id="cookie-banner" class="cookie-banner">)'
    
    replacement = r"""\1
        </div>
        
        <!-- Right Desktop Ads -->
        <div class="ad-space-desktop right-ad" style="flex: 1 1 0; min-width: 0; max-width: calc(50vw - 450px);">
            <ins class="adsbygoogle"
                 style="display:block"
                 data-ad-client="ca-pub-6859171401389344"
                 data-ad-slot="2448522751"
                 data-ad-format="auto"
                 data-full-width-responsive="true"></ins>
            <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
        </div>
    </div>
    
    <!-- Site Footer -->
    <footer class="site-footer" style="margin-top: auto; width: 100%; max-width: 800px; margin-left: auto; margin-right: auto; text-align: center;">
        <a href="index.html">Home</a>
        <a href="privacy.html">Privacy Policy</a>
        <a href="terms.html">Terms of Service</a>
        <a href="mailto:wayden2025@gmail.com">Contact Us</a>
        <p>&copy; 2026 Wall Dash. All rights reserved.</p>
    </footer>

    \2"""
    
    html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    
    with open('index.html', 'w') as f:
        f.write(html)
    print("Fixed index.html structure")


def fix_game():
    with open('game.html', 'r') as f:
        html = f.read()
    
    pattern = r'(<button onclick="window\.location\.href=\'index\.html\'"[^>]*>HOME</button>\s*</div>\s*</div>\s*</div>\s*</div>).*?(<!-- Site Footer -->)'
    
    replacement = r"""\1
        <!-- Right Desktop Ads -->
        <div class="ad-space-desktop right-ad" style="flex: 1 1 0; min-width: 0; max-width: calc(50vw - 300px);">
            <ins class="adsbygoogle"
                 style="display:block"
                 data-ad-client="ca-pub-6859171401389344"
                 data-ad-slot="2448522751"
                 data-ad-format="auto"
                 data-full-width-responsive="true"></ins>
            <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
        </div>
    </div>
    
    \2"""
    
    html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    with open('game.html', 'w') as f:
        f.write(html)
    print("Fixed game.html structure")

fix_index()
fix_game()
