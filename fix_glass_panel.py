with open('index.html', 'r') as f:
    html = f.read()

bad_string = 'class="glass-panel" style="margin: 0 auto; margin: 0 auto;" style="margin: 0 auto; max-width: 600px; padding: 40px; display: flex; flex-direction: column; align-items: center; border-radius: 15px; box-shadow: 0 0 30px rgba(0, 255, 255, 0.2);"'
good_string = 'class="glass-panel" style="margin: 0 auto; max-width: 600px; padding: 40px; display: flex; flex-direction: column; align-items: center; border-radius: 15px; box-shadow: 0 0 30px rgba(0, 255, 255, 0.2);"'

if bad_string in html:
    html = html.replace(bad_string, good_string)
    with open('index.html', 'w') as f:
        f.write(html)
    print("Fixed glass panel style.")
else:
    print("Bad string not found!")

