import pandas as pd
import numpy as np
import cv2
import sys
import os
 
def load_dataset(dataset_path):
	cols = ["path", "tempture"]
	df = pd.read_csv(dataset_path, sep=",", header=None, names=cols)
	return df

def load_images(df, resize=(64, 64)):
    images = []
    for path in df["path"]:
        p = path.split("\"")[0]
        if os.path.exists(p):
            img = cv2.imread(p)
            img = cv2.resize(img, resize)
            if img is not None:
                images.append(img)
                sys.stdout.write("\r[ * ] Loading "+str(len(images) * 100 / df.shape[0])+"% images. Remain: "+str(df.shape[0]-len(images)))
                sys.stdout.flush()
        else:
            print "[?] This '{0}' does not exist".format(p)
    print ""
    return np.array(images)
