#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Copyleft 2019 ThermoMed
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#( CopyLeft License ) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import cv2
import numpy as np

SIZEWIN     = (640, 480)
TITLE       = "Preview..."
thresh      = 50
erodeSize   = 5
dilateSize  = 7

imgSrc = '../assets/face002.jpg'
#imgSrc = '../assets/image.jpg'

vc = cv2.imread(imgSrc)
frame = vc

frame_v = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)[:,:,2]
blurredBrightness = cv2.bilateralFilter(frame_v, 9, 150, 150)
edges = cv2.Canny(blurredBrightness,thresh,thresh*2, L2gradient=True)
_, mask = cv2.threshold(blurredBrightness,200,1,cv2.THRESH_BINARY)

eroded = cv2.erode(mask, np.ones((erodeSize, erodeSize)))
mask = cv2.dilate(eroded, np.ones((dilateSize, dilateSize)))
cv2.imshow(TITLE, cv2.resize(cv2.cvtColor(mask*edges, cv2.COLOR_GRAY2RGB) | frame, SIZEWIN, interpolation = cv2.INTER_CUBIC))
cv2.waitKey(0)
