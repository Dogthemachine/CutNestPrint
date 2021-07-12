#!/usr/bin/env python3.7


import cv2
import re


def TIFF2SVG(open_tiff_path):
    # Reading image
    image = cv2.imread(open_tiff_path)

    # Converting to binary & threshold
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, im = cv2.threshold(img_gray, 254, 255, cv2.THRESH_BINARY_INV)

    # Now resizing image
    scale_percent = 48  # percent of original size
    # Defining height and width through .shape + applying scale percent
    width = int(im.shape[1] * scale_percent / 100)
    height = int(im.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)

    # Running .findContours, use the RETR_EXTERNAL flag
    contours, hierarchy = cv2.findContours(resized.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Saving contour in SVG
    save_svg_path = re.findall('.*[.]', open_tiff_path)[0] + 'svg'
    c = max(contours, key=cv2.contourArea) #max contour
    f = open(save_svg_path, 'w+')
    f.write('<?xml version="1.0" encoding="utf-8"?>' + '\n')
    f.write('<svg width="' + str(width) + 'mm' + '" height="' + str(height) + 'mm' + '\n' + '" xmlns="http://www.w3.org/2000/svg">' + '\n')
    f.write('<path d="M')

    for i in range(len(c)):
        x, y = c[i][0]
        f.write(str(x)+  ' ' + str(y)+' ')

    f.write('"/>')
    f.write('</svg>')
    f.close()

    # Cleaning memory
    del image, im, resized, contours, dim, width, height, scale_percent


if __name__ == '__main__':
    TIFF2SVG('filename.tif')