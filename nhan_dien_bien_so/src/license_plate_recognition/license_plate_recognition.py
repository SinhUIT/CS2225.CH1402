import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from .local_utils import detect_lp
from os.path import splitext, basename
from keras.models import model_from_json
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.mobilenet_v2 import preprocess_input
from sklearn.preprocessing import LabelEncoder
import glob


def load_model(path):
    try:
        path = splitext(path)[0]
        with open('%s.json' % path, 'r') as json_file:
            model_json = json_file.read()
        model = model_from_json(model_json, custom_objects={})
        model.load_weights('%s.h5' % path)
        print("Loading model successfully...")
        return model
    except Exception as e:
        print(e)


def preprocess_image(image_path, resize=False):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255
    if resize:
        img = cv2.resize(img, (224, 224))
    return img


def get_plate(model, image_path, Dmax=608, Dmin=608):
    vehicle = preprocess_image(image_path)
    ratio = float(max(vehicle.shape[:2])) / min(vehicle.shape[:2])
    for j in range(0, 50):
        try:
            Dmin = Dmin + j
            side = int(ratio * Dmin)
            bound_dim = min(side, Dmax)
            _, LpImg, _, cor = detect_lp(model, vehicle, bound_dim, lp_threshold=0.5)
            break
        except AssertionError:
            pass
    return vehicle, LpImg, cor

# test_image_path = "Plate_examples/germany_car_plate.jpg"
# vehicle, LpImg,cor = get_plate(test_image_path)
#
# fig = plt.figure(figsize=(12,6))
# grid = gridspec.GridSpec(ncols=2,nrows=1,figure=fig)
# fig.add_subplot(grid[0])
# plt.axis(False)
# plt.imshow(vehicle)
# grid = gridspec.GridSpec(ncols=2,nrows=1,figure=fig)
# fig.add_subplot(grid[1])
# plt.axis(False)
# plt.imshow(LpImg[0])
