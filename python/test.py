import cv2
import numpy as np
import matplotlib.pyplot as plt

face_cascade = cv2.CascadeClassifier('haar/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haar/haarcascade_eye.xml')

img = cv2.imread('img/ma.jpg')

histogram = cv2.calcHist([img], [0], None, [256], (0, 255))
print(histogram.shape)
print(histogram)
print(enumerate(histogram))

b, g, r = cv2.split(img)
plt.hist(b.ravel(), 256, [0, 256])
plt.hist(g.ravel(), 256, [0, 256])
plt.hist(r.ravel(), 256, [0, 256])

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray)
for x, y, w, h in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    roi_gray = gray[y:y + h, x:x + w]
    roi_color = img[y:y + h, x:x + w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for ex, ey, ew, eh in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

resized_img = cv2.resize(img, (700, 700))
cv2.imshow('Image', resized_img)
his = np.zeros((255, 256))
for x, y in enumerate(histogram):
    print(x, y)
    cv2.line(his, (x, 0), (x, y), (255, 255, 255))
plt.show()
cv2.imshow('histogram', his)
cv2.waitKey()
cv2.destroyAllWindows()
