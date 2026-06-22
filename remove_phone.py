with open('privacy.html', 'r') as f:
    privacy = f.read()

# Remove the phone number line
privacy = privacy.replace('            <li>Phone: 669-208-8714</li>\n', '')

with open('privacy.html', 'w') as f:
    f.write(privacy)
print("Phone number removed.")
