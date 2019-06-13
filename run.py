from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import numpy as np
import locale

from thermo import dataset
from thermo import model

#loading the data frame
df = dataset.load_dataset('./datasets.csv')
print "[INFO] There'is {} line in the data frame".format(df.shape[0])

print("[INFO] constructing training/testing split...")
(train, test) = train_test_split(df, test_size=0.25, random_state=42)
max_temp = 37
trainY = train["tempture"].astype(float) / max_temp
testY = test["tempture"].astype(float) / max_temp

print("[INFO] loading images...")
images = dataset.load_images(df)
images = images / 255.0

split = train_test_split(df, images, test_size=0.25, random_state=42)
(trainAttrX, testAttrX, trainImagesX, testImagesX) = split

print("[INFO] processing data...")
model = model.create_mlp(trainX.shape[1], regress=True)
opt = Adam(lr=1e-3, decay=1e-3 / 200)
model.compile(loss="mean_absolute_percentage_error", optimizer=opt)
 
# train the model
print("[INFO] training model...")
model.fit(trainX, trainY, validation_data=(testX, testY),
	epochs=200, batch_size=8)
print("[INFO] predicting tempture")
preds = model.predict(testX)
 
# compute the difference between the *predicted* house prices and the
# *actual* house prices, then compute the percentage difference and
# the absolute percentage difference
diff = preds.flatten() - testY
percentDiff = (diff / testY) * 100
absPercentDiff = np.abs(percentDiff)
 
# compute the mean and standard deviation of the absolute percentage
# difference
mean = np.mean(absPercentDiff)
std = np.std(absPercentDiff)
 
# finally, show some statistics on our model
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
print("[INFO] avg. tempture: {}, std tempture: {}".format(
	locale.currency(df["tempture"].mean(), grouping=True),
	locale.currency(df["tempture"].std(), grouping=True)))
print("[INFO] mean: {:.2f}%, std: {:.2f}%".format(mean, std))
