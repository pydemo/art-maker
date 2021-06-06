import os, sys
import cv2
import numpy as np
from os.path import join,  isfile
from pprint import pprint as pp
e=sys.exit
floc=join('images', 'mondrian.JPG')
assert isfile(floc)
img = cv2.imread(floc)
rgb_codes = img.reshape(-1, img.shape[-1])
#pp(rgb_codes)
#e()
cl=np.unique(rgb_codes, axis=0, return_counts = True)

pp(cl)
