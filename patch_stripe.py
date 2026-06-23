import re

with open('index.html', 'r') as f:
    html = f.read()

# Replace the buy button to redirect to Stripe
old_btn = r'<button id="buy-btn" onclick="processPurchase\(\)".*?>\s*Buy for \$1\.99\s*</button>'
new_btn = r"""<button id="buy-btn" onclick="window.location.href='https://buy.stripe.com/test_5kQ00c2wtfkYcQHgS42wU00'" style="background: linear-gradient(45deg, #ffaa00, #ff0055); color: #fff; border: none; padding: 15px 40px; font-size: 24px; font-weight: bold; border-radius: 30px; cursor: pointer; text-transform: uppercase; font-family: 'Courier New', Courier, monospace; box-shadow: 0 0 20px rgba(255,170,0,0.6); transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.05)';" onmouseout="this.style.transform='scale(1)';">
                Buy for $1.99
            </button>"""
html = re.sub(old_btn, new_btn, html)

# Replace the processPurchase function with the URL check logic
old_script = r"""function processPurchase\(\) \{.*?\}"""
new_script = r"""document.addEventListener("DOMContentLoaded", function() {
            // Check if user just returned from a successful Stripe checkout
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('success') === 'true') {
                localStorage.setItem('premiumBundleUnlocked', 'true');
                document.getElementById('store-modal').style.display = 'flex';
                document.getElementById('checkout-container').style.display = 'none';
                document.getElementById('success-msg').style.display = 'block';
                
                // Remove the query parameter to clean up the URL
                window.history.replaceState({}, document.title, window.location.pathname);
                
                setTimeout(() => {
                    document.getElementById('store-modal').style.display = 'none';
                    document.getElementById('checkout-container').style.display = 'flex';
                    document.getElementById('success-msg').style.display = 'none';
                }, 4000);
            }
        });"""
html = re.sub(old_script, new_script, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
print("index.html patched with Stripe logic.")
