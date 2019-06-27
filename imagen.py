import glob
import os

from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

datagen = ImageDataGenerator(
        rotation_range=45,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

paths = glob.glob("dsets/*")
for path in paths:
    print "[ * ] Generating {} files".format(path)
    prefix = os.path.basename(path.split("_")[0])
    img = load_img(path)
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape)
    i = 0
    for batch in datagen.flow(x, batch_size=1,
            save_to_dir='dsets', save_prefix=prefix, save_format='png'):
        i += 1
        if i > 20:
            break
