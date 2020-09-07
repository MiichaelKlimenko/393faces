#!/usr/bin/python3 -u
# coding: utf8
import sys
import filetype
import cgi, os
import cgitb
from cv2 import *
import cv2, os
import numpy as np
import re
import shutil
from PIL import Image
import dlib
from skimage import io
from scipy.spatial import distance
import shutil


def MYerror():
    print("Location: error.html\n")   #Файлы для вывода различных ошибок

def MYerror2():
    print("Location: error2.html\n")

tempdir = "/var/www/html/393faces/tmp/"   
cgitb.enable(display=0, logdir="/tmp/")
form = cgi.FieldStorage()
fileitem = form['file']
try:
    if fileitem.filename:
        buf = fileitem.file.read()
        size = int(sys.getsizeof(buf))
        fn = os.path.basename(fileitem.filename)
        if (size < 261) or (size > 10 * 1024 * 1024):
            MYerror()
        kind = filetype.guess(buf)

        if kind is None:
            MYerror()

        if str(kind.mime)[:5] != "image":
            MYerror()

        open(tempdir + str(fn), 'wb').write(buf)

        nums = form.getvalue("myRange2")
        nums = int(nums)/100

        sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
        detector = dlib.get_frontal_face_detector()

        FACE_DETECTOR_PATH = r'haarcascade_frontalface_default.xml'

        face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier(r'haarcascade_eye.xml')

        img = io.imread('tmp/' + str(fileitem.filename))

        dets = detector(img, 1)

        for k, d in enumerate(dets):
            shape = sp(img, d)

        face_descriptor1 = facerec.compute_face_descriptor(img, shape)

        new_desc = np.load('ex.npy')

        last_name = ''
        put = {}
        txt_desc = open('desc.txt').read().splitlines()
        last_fname = ''
        for i in range(len(txt_desc)):
            dist = distance.euclidean(face_descriptor1, new_desc[i])
            if dist < nums:
                fname = './test_pics/' + txt_desc[i]
                if last_name != fname:
                    img = imread(fname)
                    put[dist] = fname
                    # put.append(fname)
                    # cv2.imwrite('./final/' + txt_desc[i], img)
                last_name = fname
        i = 1

        keys = list(put.keys())
        keys.sort()
        
        
        #В отсортированном массиве keys содеражатся евклидовы расстояния для каждой картинки, то есть
        #чем раньше на странице расположена картинка, тем больше вероятность встретить своё лицо на ней

        #В словаре put содеражатся названия картинок и их евклидово расстояние
        #Например следующий код позволит встроить данные картинки в вашу html-страницу:

        j = 0
        for i in keys:
            if j == 0:
                print('<tr>')
                print('<td><center><br><a href="' + str(put[i]) + '" target="blank"><img src="' + str(put[i]) + '" width="90%" height="auto"></a><br></td>')
                j += 1
            else:
                print('<td><center><br><a href="' + str(put[i]) + '" target="blank"><img src="' + str(put[i]) + '" width="90%" height="auto"></a><br></td>')
                print('</tr>')
                j = 0
                
    else: MYerror()
    except Exception:
    MYerror2()


