import matplotlib.pyplot as plt

def plot(history):
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper right')
    plt.show()

    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper right')
    plt.show()

def plot_metrics(history):
    #'mse', 'mae', 'mape', 'cosine'
    plt.plot(history.history['mean_squared_error'])
    plt.plot(history.history['mean_absolute_error'])
    plt.plot(history.history['mean_absolute_percentage_error'])
    plt.plot(history.history['cosine_proximity'])
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['mse', 'mae', 'mape', 'cosine'], loc='upper right')
    plt.show()
