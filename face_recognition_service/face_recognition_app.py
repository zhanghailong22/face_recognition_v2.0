#!/usr/bin/python
# -*- coding: utf-8 -*-
# This is an app application for face recognition microservices.
# Its functions are: face upload, face recognition, Video face recognition, etc.
# The restfull api is http://127.0.0.1:9999. Database is redis, used to store
# the feature vector of the face.
# Author e-mail:zhanghailong22@huawei.com
#
import os

import video_camera
from flask import Flask, Response, request, jsonify
import redis
import face_recognition
import numpy as np

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
# pool = redis.ConnectionPool(host='redis', port=6379)
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'code': 500, 'msg': '没有文件'})

    files = request.files.getlist("file")
    for file in files:
        file_path = os.path.join('images/', file.filename)
        if file:
            file.save(file_path)
        else:
            return 'failed'
        name = file.filename[0:-4]
        image = face_recognition.load_image_file(file)
        face_locations = face_recognition.face_locations(image)
        if len(face_locations) != 1:
            return jsonify({'code': 500, 'error': '人脸数量有误'})
        face_encodings = face_recognition.face_encodings(image, face_locations)
        # 连数据库
        r = redis.Redis(connection_pool=pool)
        # 录入人名-对应特征向量
        r.set(name, face_encodings[0].tobytes())
    return jsonify({'code': 0, 'result': '录入成功'})

# 人脸搜索
@app.route('/search_images', methods=['POST'])
def search_practice():
    if 'file' not in request.files:
        return jsonify({'code': 500, 'result': '没有文件'})
    file = request.files['file']
    image = face_recognition.load_image_file(file)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    # 连数据库
    r = redis.Redis(connection_pool=pool)
    # 取出所有的人名和它对应的特征向量
    names = r.keys()
    faces = r.mget(names)
    # 组成矩阵，计算相似度（欧式距离）
    find_names = []
    number = len(face_encodings)
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces([np.frombuffer(x) for x in faces], face_encoding)
        for name, match in zip(names, matches):
            if match:
                find_names.append(name)
                break

    return jsonify({'图片中人脸的个数': number, '查询到的人脸个数': len(find_names), \
                    "find_names": [str(name, 'utf-8') for name in find_names]})
#   return jsonify({'code': 0, 'names': [str(name, 'utf-8') for name, match in zip(names, matches) if match]})

# 视频监控
@app.route('/search_video', methods=['POST'])
def search_video():
    # 连数据库
    r = redis.Redis(connection_pool=pool)
    # 取出所有的人名和它对应的特征向量
    names = r.keys()
    faces = r.mget(names)
    # 组成矩阵，计算相似度（欧式距离）
    face_names = video_camera.video_camera(names, faces)

    return jsonify({'names': face_names})

# 更新redis，将人脸图片的特征向量导入redis数据库
@app.route('/update_redis', methods=['POST'])
def update_redis():
    directory_name="images"
    # 连数据库
    r = redis.Redis(connection_pool=pool)
    for filename in os.listdir(directory_name):
        file = open(directory_name + "/" + filename, 'rb')
        name = filename[0:-4]
        image = face_recognition.load_image_file(file)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        # 录入人名-对应特征向量
        r.set(name, face_encodings[0].tobytes())
    names = r.keys()

    return jsonify({'redis中人脸数目': len(names), 'result': '更新成功'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=9999)
