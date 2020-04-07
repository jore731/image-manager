import shutil
import exif
import time
import os
import re
import concurrent.futures
import logging
import rawpy
import imageio
import matplotlib.pyplot as plt
import pandas as pd

logging.basicConfig(filename='example.log', level=logging.DEBUG)
validExtensions = ["jpg", "JPG", "NEF", "nef",
                   "PNG", "png", "TIFF", "tiff", "DNG", "dng"]
threads = []

imagePath = input("Image to analyze:")
splitted = imagePath.split(".")
try:
    extension = splitted[-1]
except:
    extension = "none"
print(extension)
data = []
if extension in validExtensions:
    with rawpy.imread(imagePath) as image_file:
        txtPath = f"{os.path.basename(imagePath)}.txt"
        f = open(txtPath, 'w+')
        processed = image_file.postprocess(
            no_auto_bright=True, use_auto_wb=False, gamma=None)
        # for index, line in enumerate(processed):
        #     for index2,data in enumerate(line):
        #         for index3, data2 in enumerate(data):
        #             if index in {0,1,2}:
        #                 processed[index,index2,index3] = 0
        #             f.write(f"{data2}")
        #     f.write(f"\n")
        processed.to_pickle("processed.pkl")
        print(processed[0])
        imageio.imwrite("test2.tiff", processed)
            #f.write(f"\n")
        with open("test.nef", "w+") as p:
            image_file = open (imagePath, "rb")
            for line in image_file:
                    p.write(f"{line}")
            
        # for value in data:
        #     print (value)
        # try:
        #     my_image = exif.Image(image_file)
        # except:
        #     print(f"{os.path.basename(imagePath)} no exif data found")
        #     print(time.ctime(os.path.getctime(imagePath)))
        #     raise EnvironmentError 

        # if(my_image.has_exif):
        #     for attribute in dir(my_image):
        #         if attribute[0] == "_":
        #             print(f"{attribute} irrelevant")
        #         else:
        #             try:
        #                 print(
        #                     f"{attribute} : {getattr(my_image,attribute)}")
        #             except:
        #                 print(f"{attribute} not printable")
        # else:
        #     print(os.path.getctime(imagePath))
