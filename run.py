from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import numpy as np
from keras.utils import to_categorical

from thermo import dataset
from thermo import model

#df = dataset.load_dataset('/content/gdrive/My Drive/Colab Notebooks/datasets.csv')
df = dataset.load_dataset('./datasets.csv')
print "[ i ] There'is {} line in the data frame".format(df.shape[0])
print "[ i ] loading images..."
images = dataset.load_images(df)
images = images / 255.0

split = train_test_split(df, images, test_size=.25, random_state=42)
(trainAttrX, testAttrX, trainImagesX, testImagesX) = split

maxTempture = trainAttrX["tempture"].max()
trainY = trainAttrX["tempture"].astype(float) / maxTempture
testY = testAttrX["tempture"].astype(float) / maxTempture
print "[ i ] processing data..."
model = model.create_cnn(64, 64, 3, regress=True)
model.compile(
        loss="mean_absolute_percentage_error",
        optimizer=Adam(0.01),
        metrics=['accuracy'])

print "[ i ] training model..."
model.fit(trainImagesX, trainY, validation_data=(testImagesX, testY),
        epochs=2, batch_size=100)
print "[ i ] predicting tempture"
preds = model.predict(testImagesX, verbose=1)
diff = preds.flatten() - testY
percentDiff = (diff / testY) * 100
absPercentDiff = np.abs(percentDiff)
mean = np.mean(absPercentDiff)
std = np.std(absPercentDiff)
print "[ * ] Mean: {:.2f}%, STD: {:.2f}%".format(mean, std)

loss, accuracy = model.evaluate(trainImagesX, trainY, verbose=1)
print "[ * ] Training Accuracy: {:.4f}, Loss: {:.4f}".format(accuracy, loss)
loss, accuracy = model.evaluate(testImagesX, testY, verbose=1)
print "[ * ] Testing Accuracy:  {:.4f}, Loss: {:.4f}".format(accuracy, loss)
model.summary()
