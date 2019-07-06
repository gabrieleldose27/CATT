from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Activation, Dropout, Dense
from keras.layers import Flatten, Input, Lambda
from keras.models import Model, Sequential

from keras.optimizers import Adam, SGD, RMSprop

def create_cnn(input_shape):
    model = Sequential()

    model.add(Lambda(lambda x: x/255.0, input_shape=input_shape))

    model.add(Conv2D(16, (7, 7),
        activation='sigmoid', strides=(2, 2)))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(8, (7, 7),
        activation='sigmoid', strides=(2, 2)))
    model.add(MaxPooling2D(pool_size=(3, 3)))

    model.add(Dropout(.33))
    model.add(Flatten())
    model.add(Dense(16, activation='sigmoid'))
    model.add(Dropout(.33))
    model.add(Dense(8, activation='sigmoid'))
    model.add(Dense(4, activation='sigmoid'))
    model.add(Dense(1, activation='linear'))
    return model

def compile(input_shape, loss="mean_absolute_percentage_error", opt=Adam(lr=0.01)):
    model = create_cnn(input_shape)
    model.compile(
            loss = loss,
            optimizer = opt,
            metrics = ['accuracy'])
    return model

def train(model, trainX, trainY, testX, testY, epochs=10, batch_size=32):
    return model.fit(
            trainX,
            trainY,
            validation_data = (testX, testY),
            epochs = epochs,
            batch_size = batch_size)

def save(model, epochs, acc):
    model.save_weights("core/h5/thermo-{}-{}.h5".format(epochs, acc))
