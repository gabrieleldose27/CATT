import argparse
import numpy as np
from sklearn.model_selection import train_test_split

from keras.optimizers import Adam, SGD, RMSprop

from generators import dataset, model, stats

def load_df(path):
    return dataset.load_dataset(path)

def test_split(df, images):
    return train_test_split(df, images, test_size=.01, random_state=42)

def predicting(model, testX, testY):
    preds = model.predict(testX, verbose=1)
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
    	help="size of resized image", default=64)
    ap.add_argument("-b", "--batch", type=int, required=False,
    	help="Batch size", default=32)
    ap.add_argument("-s", "--summary", type=bool, required=False,
    	help="show the summary of the model", default=False)

    args = ap.parse_args()
 	
    df = load_df(args.datasets)
    print "[ i ] There'is {} line in the DataFrame".format(df.shape[0])
    images = dataset.load_images(df, resize=(args.resize, args.resize))
    images = images / 255.0
    (train_x, test_x, trainX, testX) = test_split(df, images)

    maxTempture = train_x["tempture"].max()
    trainY = train_x["tempture"].astype(float) / maxTempture
    testY = test_x["tempture"].astype(float) / maxTempture

    print "[ i ] Creating the model..."
    mdl = model.compile((args.resize, args.resize, 3))
    
    print "[ i ] Training model..."
    history = model.train(mdl, trainX, trainY, testX, testY, args.epochs, args.batch)

    print "[ i ] Predicting tempture"
    mean, std = predicting(mdl, testX, testY)
    print "[ * ] Mean: {:.2f}%, STD: {:.2f}%".format(mean, std)
    
    loss, acc = mdl.evaluate(trainX, trainY, verbose=1)
    print "[ * ] Training Accuracy: {:.4f}, Loss: {:.4f}".format(acc, loss)
    loss, acc = mdl.evaluate(testX, testY, verbose=1)
    print "[ * ] Testing Accuracy:  {:.4f}, Loss: {:.4f}".format(acc, loss)

    print "[ * ] Saving the model"
    model.save(mdl, args.epochs, acc)
    
    #stats.plot_metrics(history)
    stats.plot(history)
    if args.summary:
        mdl.summary()
