This repo is used for develop app based on osdt mep
This repo is used for develop app based on osdt mep
face_recognition_service
===
This is an app application for face recognition microservices.The service was developed
on the basis of an open project for face recognition on github.The project is characterized
by the following：

Recognize and manipulate faces from Python or from the command line with the world's simplest face recognition library.

Built using dlib's state-of-the-art face recognition built with deep learning. The model has an accuracy of 99.38% on
the Labeled Faces in the Wild benchmark.

This also provides a simple face_recognition command line tool that lets you do face recognition on a folder of images
from the command line!

The face recognition microservices have the following features:face upload, face recognition, Video face recognition.

Features
===
face upload
------
Import image files with only one face into the redis database and store them in a file system named images
restful API ：curl http://127.0.0.1:9999/upload
Support multiple image files to be simultaneously upload

face recognition
------
Enter an image file with an unknown name and match the corresponding person name in the redis database
restful API ：curl http://127.0.0.1:9999/search_images
There can be multiple faces in the input image

Video face recognition
--------
Get the face video from the camera and find the name of the face in the database
restful API ：curl http://127.0.0.1:9999/search_video

update redis
------
Update the face image in the images file to the redis database

Installation
===
Requirements
-----
Python 3.6  redis
docker docker-compose
macOS or Linux (Windows not officially supported, but might work)
Installation Options:(ubuntu18.04)

Build a docker image:docker build . -t face_recognition
docker-compose.yml:docker-compose build
Pull service: docker-compose up -d
test :python3 test.py

Python Module
You can import the face_recognition module and then easily manipulate faces with just a couple of lines of code.
API Docs: https://face-recognition.readthedocs.io.


