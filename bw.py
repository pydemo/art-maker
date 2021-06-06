#!/usr/bin/env python
# -*- coding: utf-8 -*-

#./binarize.py -i convert_image.png -o result_bin.png --threshold 200

"""Binarize (make it black and white) an image with Python."""
import os
from os.path import join
from PIL import Image
#from scipy.misc import imsave

from  imageio import imwrite as imsave
#imageio.imwrite('filename.jpg', array)


import numpy
import click
click.disable_unicode_literals_warning = True
def binarize_image(img_path, target_path, threshold):
    """Binarize an image."""
    image_file = Image.open(img_path)
    image = image_file.convert('L')  # convert image to monochrome
    image = numpy.array(image)
    image = binarize_array(image, threshold)
    imsave(target_path, image)


def binarize_array(numpy_array, threshold=200):
    """Binarize a numpy array."""
    for i in range(len(numpy_array)):
        for j in range(len(numpy_array[0])):
            if numpy_array[i][j] > threshold:
                numpy_array[i][j] = 255
            else:
                numpy_array[i][j] = 0
    return numpy_array
srcd=r'C:\Users\alex_\OneDrive\Pictures\Sony7r4\Sony_135mm\5-22-2020'
fn='DSC00887.JPG'

@click.command()
@click.option('-i', 	'--input',      default = join(srcd,fn), type=str,	help = 'Input', required=True)
@click.option('-o', 	'--output',     default = fn,            type=str,	help = 'Output', required=True)
@click.option('-t', 	'--threshold',  default = 200,           type=int,	help = 'threshold', required=True)
def main(**kwargs):

    binarize_image(kwargs['input'], '%d_%s' % (kwargs['threshold'], kwargs['output']), kwargs['threshold'])
if __name__ == "__main__":
    main()