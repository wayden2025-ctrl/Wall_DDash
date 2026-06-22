import re

email = "wayden2025@gmail.com"
phone = "669-208-8714"

with open('privacy.html', 'r') as f:
    privacy = f.read()
contact_pattern = r"<p>If you have any questions about this Privacy Policy, you can contact us at: contact@walldash\.com</p>"
contact_replacement = f"<p>If you have any questions about this Privacy Policy, you can contact us at:</p>\n        <ul>\n            <li>Email: {email}</li>\n            <li>Phone: {phone}</li>\n        </ul>"
privacy = re.sub(contact_pattern, contact_replacement, privacy)
with open('privacy.html', 'w') as f:
    f.write(privacy)

for filename in ['index.html', 'game.html']:
    with open(filename, 'r') as f:
        html = f.read()
    html = html.replace('mailto:contact@walldash.com', f'mailto:{email}')
    with open(filename, 'w') as f:
        f.write(html)
print("Updated contact info.")
