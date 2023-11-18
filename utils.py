import json

import os
from PIL import Image

import os
import selenium
from selenium import webdriver 
import base64
import time
import urllib.request

def removeCorruptedImages(path: str) -> None:
    img_dir = r"path"
    for filename in os.listdir(img_dir):
        try :
            with Image.open(img_dir + "/" + filename) as im:
                print('ok')
        except :
            print(img_dir + "/" + filename)
            os.remove(img_dir + "/" + filename)


def dump_to_text(l:list) -> str:
    return json.dumps(l)

def dump_to_list(s: str) -> list:
    return json.loads(s)


def scrapFirstImageFromGoogle(searchKey: str) -> None:
    SAVE_FOLDER = 'foodImages/'

    GOOGLE_IMAGES = 'https://images.google.com'

    driver = webdriver.Chrome()
    driver.get(GOOGLE_IMAGES)
    counter = 0
    for i in range(1,2):
        image_elements = driver.find_elements_by_class_name('rg_i')
        print(len(image_elements))