# image processing 
import numpy as np
from PIL import Image
import math


# threshold value = 20

def read_image(file_path):
    im = Image.open('penguins.jpg')
    pix = im.load()
    width = im.size[0]
    height = im.size[1]
    rgba = pix[width, height]
    
    
    

    
    







def main():
    print("Hello from quadtree-image!")
    
    




















if __name__ == "__main__":
    main()
