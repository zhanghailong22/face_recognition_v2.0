import requests
from flask import Flask, Response, request, jsonify

url = "http://127.0.0.1:9999/upload"

filepath = 'D:\code_input_gitlab\osdt-mep-app\examples/biden.jpg'
split_path = filepath.split('/')
filename = split_path[-1]
print(filename)

file = open(filepath, 'rb')
files = {'file': (filename, file, 'image/jpg')}

r = requests.post(url, files=files)
result = r.text

url = "http://127.0.0.1:9999/search_images"

filepath = 'D:\code_input_gitlab\osdt-mep-app\examples/alex-lacamoire.png'
split_path = filepath.split('/')
filename = split_path[-1]
print(filename)

file = open(filepath, 'rb')
files = {'file': (filename, file, 'image/jpg')}

r = requests.post(url, files=files)
result = r.text
print(result)

url = "http://127.0.0.1:9999/search_video"

r = requests.post(url)
result = r.text
print(result)

url = "http://127.0.0.1:9999/update_redis"

r = requests.post(url)
result = r.text
print(result)