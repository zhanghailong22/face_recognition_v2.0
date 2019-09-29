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
Import image files with only one face into the redis database and store them in a file system named images<br>
restful API ：curl http://127.0.0.1:9999/upload<br>
Support multiple image files to be simultaneously upload

face recognition
------
Enter an image file with an unknown name and match the corresponding person name in the redis database<br>
restful API ：curl http://127.0.0.1:9999/search_images<br>
There can be multiple faces in the input image

Video face recognition
--------
Get the face video from the camera and find the name of the face in the database<br>
restful API ：curl http://127.0.0.1:9999/search_video

update redis
------
Update the face image in the images file to the redis database

Installation
===
Requirements
-----
Python 3.6  redis dlib face_recognition<br>
docker docker-compose<br>
macOS or Linux (Windows not officially supported, but might work)<br>
Installation Options:(ubuntu18.04)<br>
Third party library:dlib face_recognition flask redis opencv-python requests 

Build a docker image:docker build . -t face_recognition<br>
docker-compose.yml:docker-compose build<br>
Pull service: docker-compose up -d<br>
test :python3 test.py

Python Module
----
You can import the face_recognition module and then easily manipulate faces with just a couple of lines of code.<br>
API Docs: https://face-recognition.readthedocs.io.


