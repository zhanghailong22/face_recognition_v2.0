#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

import video_camera
from flask import Flask, Response, request, jsonify
import redis
import face_recognition
import numpy as np


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
#pool = redis.ConnectionPool(host='redis', port=6379)
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
            return jsonify({'code': 500, 'msg': '人脸数量有误'})
        face_encodings = face_recognition.face_encodings(image, face_locations)
        # 连数据库
        r = redis.Redis(connection_pool=pool)
        # 录入人名-对应特征向量
        r.set(name, face_encodings[0].tobytes())
    return jsonify({'code': 0, 'msg': '录入成功'})
#人脸搜索
@app.route('/search_images', methods=['POST'])
def search_practice():
    if 'file' not in request.files:
        return jsonify({'code': 500, 'msg': '没有文件'})
    file = request.files['file']
    image = face_recognition.load_image_file(file)
    face_locations = face_recognition.face_locations(image)
    if len(face_locations) != 1:
        return jsonify({'code': 500, 'msg': '人脸数量有误'})
    face_encodings = face_recognition.face_encodings(image, face_locations)
    # 连数据库
    r = redis.Redis(connection_pool=pool)
    # 取出所有的人名和它对应的特征向量
    names = r.keys()
    faces = r.mget(names)
    # 组成矩阵，计算相似度（欧式距离）
    matches = face_recognition.compare_faces([np.frombuffer(x) for x in faces], face_encodings[0])
    for name, match in zip(names, matches):
        if match:
            return jsonify({'result': 'success', 'names': str(name, 'utf-8')})
        else:
            return jsonify(({'result': 'failed', 'name': 'Did not find the name of the person'}))

 #   return jsonify({'code': 0, 'names': [str(name, 'utf-8') for name, match in zip(names, matches) if match]})


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
#更新redis
@app.route('/update_redis', methods=['POST'])
def update_redis():
    directory_name="images"
    for filename in os.listdir(directory_name):
        file = open(directory_name + "/" + filename, 'rb')
        name = filename[0:-4]
        image = face_recognition.load_image_file(file)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        # 连数据库
        r = redis.Redis(connection_pool=pool)
        # 录入人名-对应特征向量
        r.set(name, face_encodings[0].tobytes())
    return jsonify({'code': 0, 'msg': '更新成功'})

if __name__ == '__main__':

    app.run(host="0.0.0.0", debug=True, port=9999)
