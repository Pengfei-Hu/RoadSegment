import cv2
import pandas as pd
from skimage import morphology
import numpy as np
import glob
import os


def skeleton_gen(img_path):
    img = cv2.imread(img_path,0)
    img[img==255] = 1
    skeleton0 = morphology.skeletonize(img)
    skeleton = skeleton0.astype(np.uint8)*255
    road_length = np.sum(skeleton == 255)
    print(road_length)
    pic_length_path = img_path.replace('.png', '_length.png')
    cv2.imwrite(pic_length_path, skeleton)
    return road_length, pic_length_path



