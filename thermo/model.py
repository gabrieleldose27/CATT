# import the necessary packages
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Activation, Dropout, Dense
from keras.layers import Flatten, Input, Lambda
from keras.models import Model, Sequential

def create_cnn(width, height, depth, filters=(16, 32, 64), regress=False):
#    input_shape = (height, width, depth)
#    model = Sequential()
#    model.add(Lambda(lambda x: x/127.5-1.0, input_shape=input_shape))
#    model.add(Conv2D(24, (5, 5), activation='elu', subsample=(2, 2)))
#    model.add(Conv2D(36, (5, 5), activation='elu', subsample=(2, 2)))
#    model.add(Conv2D(48, (5, 5), activation='elu', subsample=(2, 2)))
#    model.add(Conv2D(64, (3, 3), activation='elu'))
#    model.add(Conv2D(64, (3, 3), activation='elu'))
#    model.add(Dropout(0.5))
#    model.add(Flatten())
#    model.add(Dense(100, activation='elu'))
#    model.add(Dense(50, activation='elu'))
#    model.add(Dense(10, activation='elu'))
#    model.add(Dense(1))
#    return model
    chan_dim = -1
    inputs = Input(shape=(width, height, depth))
    for (i, f) in enumerate(filters):
        if i == 0:
            x = inputs
        x = Conv2D(f, (5, 5), padding="same")(x)
        x = Activation("elu")(x)
        x = BatchNormalization(axis=chan_dim)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)
    x = Flatten()(x)
    x = Dense(4)(x)
    x = Activation("elu")(x)
    x = BatchNormalization(axis=chan_dim)(x)
    x = Dropout(0.5)(x)
    x = Dense(4)(x)
    x = Activation("elu")(x)
    if regress:
    	x = Dense(1, activation="linear")(x)
    model = Model(inputs, x)
    return model
