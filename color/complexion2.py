import cv2
import os
import numpy as np
from face import skin

def hex_to_rgb(hex):
    # use to remove till # in hex 
    hex=hex.lstrip("#")

    # #855341 to r=hex 85 becomes decimal 133
    r= int(hex[0:2], 16)
    g= int(hex[2:4], 16)
    b= int(hex[4:6], 16)

    return r,g,b

def rgb_to_lab(r,g,b):
    # image matrix structure of opencv 
    # (height, width, channel) = (1,1,3)
    rgb= np.array([[[r,g,b]]], dtype=np.uint8)
    #convert rgb to lab 
    lab= cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)

    return lab[0,0]

def get_complexion(L):
    #L is brightness which is used for complexity
    if L < 100: 
        return "Dark"
    elif L < 170: 
        return "Medium"
    else: 
        return "Light"

def undertone(a,b):
    # a and b are redness and blueness which is used for tone 
    ratio = b/a 

    if ratio > 0.95:
        return "Warm"
    elif ratio < 0.75:
        return "Cool"
    else:
        return "Neutral"

def analyze(hex):

    r,g,b= hex_to_rgb(hex)
    lab=rgb_to_lab(r,g,b)
    L,a,b= lab
    comp=get_complexion(L)
    under=undertone(a,b)

    return comp,under,lab 

if __name__ == "__main__":

    hex= skin("man2.jpg")
    c,u,l= analyze(hex)

    print("Estimated HEX : ",hex)
    print("Estimated complexity : ",c)
    print("Estimated undertone : ",u)




