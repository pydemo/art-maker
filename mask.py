from PIL import Image
import numpy as np
import cv2

image = Image.open('image1.jpg')
image = np.array(image) 

redImg = np.zeros(image.shape, image.dtype)
redImg[:,:] = (0, 0, 255)
redMask = cv2.bitwise_and(redImg, redImg, mask=mask)
cv2.addWeighted(redMask, 1, image, 1, 0, image)


