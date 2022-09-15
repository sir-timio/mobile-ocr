import requests

img = 'tests/test_data/slide-1.jpeg'

inference_url = 'http://127.0.0.1:8080/predict'

with open(img, 'rb') as f:
    data = f.read()

res = requests.post(url=inference_url, data=data)
print(res.text)
