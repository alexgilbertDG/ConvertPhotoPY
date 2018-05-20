#!/usr/bin/env python
from __future__ import division
import os
import sys
from PIL import Image
import unicodedata


# args =>
# [0] = convertPicture
# [1] => format_in
# [2] => format_out
# [3] => size_out
# [4] => quality of picture

def remove_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


def clean_file_name(filename, ext):
	return remove_accents(filename).replace('.', '-').replace(' ', '').replace('(', '-').replace(')', '-') + '.' + ext


if len(sys.argv) != 5:
    print "Arguments error!"
    print "Please provide the format in, the format out, the max size wanted and the quality of picture out"
    exit(-1)

format = ['jpg', 'png', 'tif', 'gif']
output_folder = '/output/'
format_in = []
quality = 100
size_out = 1200
try:
    size_out = int(sys.argv[3])
    quality = int(sys.argv[4])
except:
    print "Your 2 last arguments need to be a integer to represent the max size of the images out and the quality"
    exit(-1)

format_in.append(sys.argv[1])
format_out = sys.argv[2]

#add variables in the naming of file
if 'jpg' in format_in:
    format_in.append('jpeg')
if 'tif' in format_in:
    format_in.append('tiff')

if 'jpg' in format_out or 'jpeg' in format_out :
    format_out = "JPEG"
if 'png' in format_out:
    format_out = "PNG"



yourpath = os.getcwd()
output_path = yourpath + '/output/'
images_path = yourpath + '/images/'
for root, dirs, files in os.walk(images_path, topdown=False):
    for name in files:
        if os.path.splitext(os.path.join(root, name))[1].lower().replace('.', '') in format_in:
            if os.path.isfile(os.path.splitext(os.path.join(root, name))[0] + ("_out" + format_out )):
                print "A {0} file already exists for {1} ".format(format_out, name)
                continue
            
            else:
                outfile = os.path.splitext(os.path.join(output_path, name))[0]
                try:
                    im = Image.open(os.path.join(root, name))
                    resize_img = None
                    print "Generating {0} for {1} at {2}".format(format_out, name, im.size)
                    if im.size[0] > (size_out+1) or im.size[1] > (size_out+1):
                        if im.size[0] > im.size[1]: #Landscape image
                            ratio = im.size[1] / im.size[0]
                            resize_img = im.resize( (int(size_out), int(size_out * ratio) ), Image.ANTIALIAS)
                        else: #portrait image
                            ratio = im.size[0] / im.size[1]
                            resize_img = im.resize( (int(size_out * ratio) ,int(size_out)), Image.ANTIALIAS)
                    else:
                        resize_img = im.resize(im.size, Image.ANTIALIAS)
                    resize_img.save(clean_file_name(outfile, 'jpg'), format_out, quality=quality)
                except Exception, e:
                    print e

        else:
            print "No images found with your format in : {0} ".format(format_in[0])