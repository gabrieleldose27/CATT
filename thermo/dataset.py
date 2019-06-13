import pandas as pd
import numpy as np
import cv2
import os
import sys
 
def load_dataset(dataset_path):
	# initialize the list of column names in the CSV file and then
	# load it using Pandas
	cols = ["path", "tempture"]
	df = pd.read_csv(dataset_path, sep=",", header=None, names=cols)
	return df

def load_images(df):
    images = []
    for path in df["path"]:
        p = path.split("\"")[0]
        if os.path.exists(p):
            img = cv2.imread(p)
            if img is not None:
                images.append(img)
                sys.stdout.write("\rloading "+str(len(images))+" images")
                sys.stdout.flush()
        else:
            print "Not existe: {}".format(p)
    print ""
    return np.array(images)




"""
def process_tempture(df, train, test):
	# initialize the column names of the continuous data
	continuous = ["path"]
	# performin min-max scaling each continuous feature column to
	# the range [0, 1]
	cs = MinMaxScaler()
	trainContinuous = cs.fit_transform(train[continuous])
	testContinuous = cs.transform(test[continuous])
	# one-hot encode the zip code categorical data (by definition of
	# one-hot encoing, all output features are now in the range [0, 1])
	zipBinarizer = LabelBinarizer().fit(df["tempture"])
	trainCategorical = zipBinarizer.transform(train["tempture"])
	testCategorical = zipBinarizer.transform(test["tempture"])
 
	# construct our training and testing data points by concatenating
	# the categorical features with the continuous features
	trainX = np.hstack([trainCategorical, trainContinuous])
	testX = np.hstack([testCategorical, testContinuous])
 
	# return the concatenated training and testing data
	return (trainX, testX)
"""
