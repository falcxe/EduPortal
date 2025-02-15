import requests
import time

while True:
    try:
        response = requests.get('https://eduportal-d2gf.onrender.com/')
        print(f'Ping status: {response.status_code}')
    except Exception as e:
        print(f'Error: {e}')
    time.sleep(840)  # 14 минут