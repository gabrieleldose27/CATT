import cv2
import os
import numpy as np

IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS = 240, 320, 3
INPUT_SHAPE = (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS)


def load_image(data_dir, image_file):
    """
    Load RGB images from a file
    """
    return cv2.imread(os.path.join(data_dir, image_file.strip()))


def preprocess(image):
    """
    Combine all preprocess functions into one
    """
    image = image[60:-25, :, :]
    image = cv2.resize(image, (IMAGE_WIDTH, IMAGE_HEIGHT), cv2.INTER_AREA)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
    return image

class AugData(list):

    def __new__(cls, data_dir, center, tempture, range_x=100, range_y=10):
        image, tempture = cls.random_choose(data_dir, center, tempture)
        image, tempture = cls.random_flip(image, tempture)
        image, tempture = cls.random_translate(image, tempture, range_x, range_y)
        image = cls.random_shadow(image)
        image = cls.random_brightness(image)
        return super().__new__(cls, [image, tempture])

    def random_choose(data_dir, center, tempture):
        return load_image(data_dir, center), tempture

    def random_flip(image, tempture):
        if np.random.rand() < 0.5:
            image = cv2.flip(image, 1)
            tempture = -tempture
        return image, tempture

    def random_translate(image, tempture, range_x, range_y):
        trans_x = range_x * (np.random.rand() - 0.5)
        trans_y = range_y * (np.random.rand() - 0.5)
        tempture += trans_x * 0.002
        trans_m = np.float32([[1, 0, trans_x], [0, 1, trans_y]])
        height, width = image.shape[:2]
        image = cv2.warpAffine(image, trans_m, (width, height))
        return image, tempture

    def random_shadow(image):
        x1, y1 = IMAGE_WIDTH * np.random.rand(), 0
        x2, y2 = IMAGE_WIDTH * np.random.rand(), IMAGE_HEIGHT
        xm, ym = np.mgrid[0:IMAGE_HEIGHT, 0:IMAGE_WIDTH]

        mask = np.zeros_like(image[:, :, 1])
        mask[(ym - y1) * (x2 - x1) - (y2 - y1) * (xm - x1) > 0] = 1

        cond = mask == np.random.randint(2)
        s_ratio = np.random.uniform(low=0.2, high=0.5)

        # adjust Saturation in HLS(Hue, Light, Saturation)
        hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
        hls[:, :, 1][cond] = hls[:, :, 1][cond] * s_ratio
        return cv2.cvtColor(hls, cv2.COLOR_HLS2RGB)

    def random_brightness(image):
        """
        Randomly adjust brightness of the image.
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        ratio = 1.0 + 0.4 * (np.random.rand() - 0.5)
        hsv[:, :, 2] = hsv[:, :, 2] * ratio
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

def batch_generator(data_dir, image_paths, temptures, batch_size, is_training):

    images = np.empty([batch_size, IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS])
    temptures = np.empty(batch_size)
    while True:
        i = 0
        for index in np.random.permutation(image_paths.shape[0]):
            center, left, right = image_paths[index]
            tempture = temptures[index]
            # argumentation
            if is_training and np.random.rand() < 0.6:
                image, tempture = AugData(data_dir, center, tempture)
            else:
                image = load_image(data_dir, center)
            images[i] = preprocess(image)
            temptures[i] = tempture
            i += 1
            if i == batch_size:
                break
        yield images, temptures
