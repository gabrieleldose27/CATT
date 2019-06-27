import argparse

import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

from keras.utils import to_categorical
from keras.optimizers import Adam, SGD, RMSprop

from thermo import dataset
from thermo import model

batch_size = 100

def load_df(path):
    return dataset.load_dataset(path)

def test_split(df, images):
    return train_test_split(df, images, test_size=.05, random_state=42)

def predicting(model, testImagesX, testY):
    preds = model.predict(testImagesX, verbose=1)
    diff = preds.flatten() - testY
    percentDiff = (diff / testY) * 100
    absPercentDiff = np.abs(percentDiff)
    mean = np.mean(absPercentDiff)
    std = np.std(absPercentDiff)
    return mean, std

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--epochs", type=int, required=False,
    	help="Number of epochs", default=2)
    ap.add_argument("-d", "--datasets", type=str, required=False,
    	help="Path to datasets", default="./datasets.csv")
    ap.add_argument("-r", "--resize", type=int, required=False,
    	help="zise of resized image", default=64)
    args = vars(ap.parse_args())

    df = load_df(args["datasets"])
    print "[ i ] There'is {} line in the DataFrame".format(df.shape[0])
    images = dataset.load_images(df, resize=(args["resize"], args["resize"]))
    images = images / 255.0
    (trainAttrX, testAttrX, trainImagesX, testImagesX) = test_split(df, images)

    maxTempture = trainAttrX["tempture"].max()
    trainY = trainAttrX["tempture"].astype(float) / maxTempture
    testY = testAttrX["tempture"].astype(float) / maxTempture
    print "[ i ] Creating the model..."

    model = model.create_cnn(args["resize"], args["resize"], 3, regress=True)
    model.compile(
            loss="mean_squared_error",
            optimizer = RMSprop(lr=0.001),
            metrics=['accuracy'])
    
    print "[ i ] Training model..."
    history = model.fit(trainImagesX, trainY, validation_data=(testImagesX, testY),
            epochs=args["epochs"], batch_size=100)

    print "[ i ] Predicting tempture"
    mean, std = predicting(model, testImagesX, testY)
    print "[ * ] Mean: {:.2f}%, STD: {:.2f}%".format(mean, std)
    
    loss, accuracy = model.evaluate(trainImagesX, trainY, verbose=1)
    print "[ * ] Training Accuracy: {:.4f}, Loss: {:.4f}".format(accuracy, loss)
    loss, accuracy = model.evaluate(testImagesX, testY, verbose=1)
    print "[ * ] Testing Accuracy:  {:.4f}, Loss: {:.4f}".format(accuracy, loss)

    print "[ * ] Saving the model"
    model.save_weights('h5/thermo-'+str(args["epochs"])+'-'+str(accuracy)+'.h5')

    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
#    model.summary()
