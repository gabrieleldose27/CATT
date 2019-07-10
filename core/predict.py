import argparse
import os
import numpy as np
from keras.models import load_model

def load_image(path):
    import cv2
    im = cv2.imread(path)
    im = cv2.resize(im, (64, 64))
    npim = np.resize(im, (1, 64, 64, 3))
    return npim

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", type=str, required=True,
    	help="path to image", default="")
    args = ap.parse_args()
    path = os.getcwd()+'/'+args.image
    if os.path.exists(path):
        print "[ ! ] Predicting on {}".format(path)
        model = load_model('./h5/catt-5-0.07.h5')
        image = load_image(path)
        image = image / 255.0
        preds = model.predict(image, verbose=1)
        maxT = 38.5
        p = preds[0][0]
        print "[ * ] Result: {:.2f}".format(p*maxT)
