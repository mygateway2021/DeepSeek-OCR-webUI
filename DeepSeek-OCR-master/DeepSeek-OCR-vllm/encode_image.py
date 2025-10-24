import base64

with open('app-icon.png', 'rb') as f:
    data = f.read()
    b64 = base64.b64encode(data).decode()
    print(f'data:image/png;base64,{b64}')