from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Activation, Dropout, Dense
from keras.layers import Flatten, Input, Lambda
from keras.models import Model, Sequential

def create_cnn(width, height, depth, filters=(16, 32, 64), regress=False):
    input_shape = (height, width, depth)
#    chanDim = -1
#    inputs = Input(shape=input_shape)
#
#    # loop over the number of filters
#    for (i, f) in enumerate(filters):
#        # if this is the first CONV layer then set the input
#        # appropriately
#        if i == 0:
#        	x = inputs
#        
#        # CONV => RELU => BN => POOL
#        x = Conv2D(f, (5, 5), padding="same")(x)
#        x = Activation("elu")(x)
#        x = BatchNormalization(axis=chanDim)(x)
#        x = MaxPooling2D(pool_size=(2, 2))(x)
#
#    x = Flatten()(x)
#    x = Dense(16)(x)
#    x = Activation("elu")(x)
#    x = BatchNormalization(axis=chanDim)(x)
#    x = Dropout(0.5)(x)
#    
#    # apply another FC layer, this one to match the number of nodes
#    # coming out of the MLP
#    x = Dense(4)(x)
#    x = Activation("elu")(x)
#    
#    # check to see if the regression node should be added
#    if regress:
#    	x = Dense(1, activation="linear")(x)
#    
#    # construct the CNN
#    model = Model(inputs, x)
#    
#    # return the CNN
#    return model
    model = Sequential()

    model.add(Lambda(lambda x: x/255.0, input_shape=input_shape))

    model.add(Conv2D(64, (3, 3), kernel_initializer='uniform', activation='elu', strides=(2, 2)))
    model.add(Conv2D(32, (3, 3), kernel_initializer='uniform', activation='elu', strides=(2, 2)))
    model.add(Conv2D(16, (3, 3), kernel_initializer='uniform', activation='elu', strides=(2, 2)))

    model.add(Dropout(.5))
    model.add(Flatten())
    model.add(Dense(4, activation='elu'))
    model.add(Dense(1))
    return model
