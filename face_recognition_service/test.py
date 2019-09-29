#!/usr/bin/python
# -*- coding: utf-8 -*-
# test face_recognition_app.py

import requests
from flask import Flask, Response, request, jsonify

# 录入
url = "http://127.0.0.1:9999/upload"

filepath = 'D:\code_input_gitlab\osdt-mep-app\examples/biden.jpg'
split_path = filepath.split('/')
filename = split_path[-1]
print(filename)

file = open(filepath, 'rb')
files = {'file': (filename, file, 'image/jpg')}

r = requests.post(url, files=files)
result = r.text

# 查询
url = "http://127.0.0.1:9999/search_images"

filepath = 'D:\code_input_gitlab\osdt-mep-app\examples/two_people.jpg'
split_path = filepath.split('/')
filename = split_path[-1]
print(filename)

file = open(filepath, 'rb')
files = {'file': (filename, file, 'image/jpg')}

r = requests.post(url, files=files)
result = r.text
print(result)

# 视频
url = "http://127.0.0.1:9999/search_video"

r = requests.post(url)
result = r.text
print(result)

# 更新redis
url = "http://127.0.0.1:9999/update_redis"

r = requests.post(url)
result = r.text
print(result)