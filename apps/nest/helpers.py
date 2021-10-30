from PIL import Image
Image.MAX_IMAGE_PIXELS = 1000000000
from PIL import ImageDraw, ImageFilter, ImageChops
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from django.conf import settings
from zipfile import ZipFile
from potrace import Bitmap
from numpy import asarray
import drawSvg as draw
import PIL.ImageOps
import numpy as np
import svgwrite
import datetime
import smtplib
import cv2
import os
import re


def TIFF2SVG(open_tiff_path, save_svg_path):
    image = cv2.imread(open_tiff_path)
    # Converting to binary & threshold
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, im = cv2.threshold(img_gray, 254, 255, cv2.THRESH_BINARY_INV)
    # Now resizing image
    # scale_percent = 48  # percent of original size
    scale_percent = 100
    # Defining height and width through .shape + applying scale percent
    width = int(im.shape[1] * scale_percent / 100)
    height = int(im.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)
    # Running .findContours, use the RETR_EXTERNAL flag
    contours, hierarchy = cv2.findContours(resized.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key=cv2.contourArea) #max contour
    # Pulling out the first point of path
    first_point = list(c)[0]
    # Writing svg content
    f = open(save_svg_path, 'w+')
    f.write('<svg width="'+str(width)+'" height="'+str(height)+'" viewBox="0 0 '+str(width)+' '+str(height)+'" xmlns="http://www.w3.org/2000/svg">')
    f.write('<path d="M')
    for i in range(len(c)):
        x, y = c[i][0]
        f.write(str(x)+' ' + str(y)+' ')
    for i in range(len(first_point)):
        x, y = c[i][0]
        f.write(str(x)+' ' + str(y)+' ')
    f.write('" stroke="black" fill="none" stroke-linejoin="round" />')
    f.write("</svg>")
    f.close()
    # Cleaning memory
    del image, im, resized, contours, dim, width, height, scale_percent, c, first_point



def TIFF2MASK(open_tiff_path):
    # Reading image
    image = cv2.imread(open_tiff_path)
    # Converting to binary & threshold
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, im = cv2.threshold(img_gray, 254, 255, cv2.THRESH_BINARY_INV)
    # Now resizing image
    scale_percent = 100  # percent of original size
    # Defining height and width through .shape + applying scale percent
    width = int(im.shape[1] * scale_percent / 100)
    height = int(im.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)
    # Running .findContours, use the RETR_EXTERNAL flag
    contours, hierarchy = cv2.findContours(resized.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Making mask like array object
    mask = np.ones(resized.shape[:2], dtype="uint8") * 255
    cv2.drawContours(mask, contours, -1, 0, -1)
    mask = Image.fromarray(mask)
    mask = PIL.ImageOps.invert(mask)
    del image, ret, im, img_gray, width, height, scale_percent, dim, resized
    return mask


def TIFF2BACKGROUND(open_tiff_path, background, x_position, y_position, rotation):
    # Reading image with Pillow
    img = Image.open(open_tiff_path)
    image_width, image_height = img.size
    # Making mask from same image by OpenCV & Pillow
    mask = TIFF2MASK(open_tiff_path)
    mask = mask.resize((image_width, image_height), Image.ANTIALIAS)
    # Mixing image + mask + background
    workspace = Image.open(background)
    workspace.paste(img.rotate(rotation), (x_position,y_position), mask.rotate(rotation))
    workspace.save(background)
    # Clearing memory
    del img, background, mask, image_width, image_height


def GETMATIREALAMOUNT(open_final_tiff_path):
    img = Image.open(open_final_tiff_path)
    image_width, image_height = img.size
    material_amount = int(image_width / 59.055)
    return material_amount


def SENDTFIFF(password, from_address, to_address, open_final_tiff_path):
    # make a name for new zip file
    zip_file_path = re.findall('[/].*[.]', open_final_tiff_path)[0] + "zip"
    # make an ZipFile object
    sanding_file = ZipFile(zip_file_path, 'w')
    # add tiff file to zip
    sanding_file.write(open_final_tiff_path)
    # close
    sanding_file.close()
    # create message object instance
    msg = MIMEMultipart()
    # setup the parameters of the message
    password = password
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Photos"
    # attach image to message body
    msg.attach(MIMEImage(zip_file_path("file").read()))
    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


def MAKEBACKGROUND(width_in_cm, height_in_sm):
    # Making .tiff background with PIL
    mode = "CMYK"
    # Resolution 150 pixels per inch
    width_background = int(width_in_cm * 59.055)
    height_background = int(height_in_sm * 59.055)
    color = (0, 0, 0, 0)
    background = Image.new(mode, (width_background, height_background), color)
    path_to_save_tif = settings.MEDIA_RESULT_ORDERS + "/" + datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S") + ".tif"
    background.save(path_to_save_tif)
    # Making .svg background with DrawSvg
    path_to_save_svg = settings.MEDIA_RESULT_CONTOUR + "/" + "BACKGROUND" + ".svg"
    f = open(path_to_save_svg, 'w+')
    f.write('<?xml version="1.0" encoding="UTF-8"?> \n <svg xmlns="http://www.w3.org/2000/svg" \
    xmlns:xlink="http://www.w3.org/1999/xlink" \n \
    width="{0}" height="{1}" viewBox="0 0 {0} {1}"> \n <defs> \n </defs> \n <rect y="0" x="0" width="{0}" height="{1}"\
    fill="None"> \n <title>BACKGROUND</title> \n </rect> \n </svg>'.format(width_background, height_background))
    f.close()
    return path_to_save_tif


def GETPOSITION(obj, filename):

    class Piece:
        def __init__(self):
            self.rot = 0
            self.x = 0
            self.y = 0

    res = Piece()

    def GETITNOW(obj, res, filename):

        svg_scale = 2.834645669291339

        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    GETITNOW(v, res, filename)
                elif k == "filename" and v == filename:
                    res.rot = obj["rotation"]
                    res.x = int(obj["x"])
                    res.y = int(obj["y"])
        elif isinstance(obj, list):
            for item in obj:
                GETITNOW(item, res, filename)
        return res

    res = GETITNOW(obj, res, filename)
    return res


def CUTWHITESPACE(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


