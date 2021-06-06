import cv2  # import OpenCV
import numpy
from blend_modes import soft_light

# Import background image
background_img_float = cv2.imread('im1.png',-1).astype(float)

# Import foreground image
foreground_img_float = cv2.imread('im2.png',-1).astype(float)

# Blend images
opacity = 0.7  # The opacity of the foreground that is blended onto the background is 70 %.
blended_img_float = soft_light(background_img_float, foreground_img_float, opacity)

# Display blended image
blended_img_uint8 = blended_img_float.astype(numpy.uint8)  # Convert image to OpenCV native display format
cv2.imshow('window', blended_img_uint8)
cv2.waitKey()  # Press a key to close window with the image.