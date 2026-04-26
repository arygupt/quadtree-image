# image processing 
import numpy as np
from PIL import Image
import math


FILE_PATH = 'penguins.jpg'


# if it is uniform, that entire thing can be represented by one color
def is_uniform(FILE_PATH, x, y, width, height, threshold=20):
    first_pixel = FILE_PATH.getpixel((x, y))
    r0, g0, b0 = first_pixel
    for row in range(y, y + height):
        for col in range(x, x + height):
            r, g, b = FILE_PATH.getpixel((col, row))
            
            difference = abs(r - r0) + abs(g - g0) + abs(b - b0)
            
            if difference > threshold:
                return False
    return True
    
    

def main():
    print("Hello from quadtree-image!")
    
    




















if __name__ == "__main__":
    main()
