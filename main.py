# image processing 
import numpy as np
from PIL import Image


FILE_PATH = 'penguins.jpg'


class QuadtreeNode:
    pass


class QuadtreeCompressor:
    def __init__(self, path, threshold=20):
        self.path = path
        self.threshold = threshold
        self.image = Image.open(path).convert("RGB")

    def is_uniform(self, x, y, width, height):
        img = self.image
        r0, g0, b0 = img.getpixel((x, y))
        for row in range(y, y + height):
            for col in range(x, x + width):
                r, g, b = img.getpixel((col, row))
                difference = abs(r - r0) + abs(g - g0) + abs(b - b0)
                if difference > self.threshold:
                    return False
        return True

    def split_if_uniform(self, x=0, y=0, width=None, height=None):
        # Uniform region: no split. Else four quadrants: TL, TR, BL, BR.
        w = self.image.width if width is None else width
        h = self.image.height if height is None else height
        if self.is_uniform(x, y, w, h):
            return None
        w1, w2 = w // 2, w - w // 2
        h1, h2 = h // 2, h - h // 2
        if w1 < 1 or w2 < 1 or h1 < 1 or h2 < 1:
            return None
        img = self.image

        def crop_at(xx, yy, ww, hh):
            return img.crop((xx, yy, xx + ww, yy + hh))

        return (
            crop_at(x, y, w1, h1),
            crop_at(x + w1, y, w2, h1),
            crop_at(x, y + h1, w1, h2),
            crop_at(x + w1, y + h1, w2, h2),
        )


class QuadtreeDecompressor:
    pass


class ImageCodec:
    pass
    
    
    
def main():
    
    img = Image.open(FILE_PATH)
    width, height = img.size
    right_top = img.crop((width/2, 0, width, height/2))
    right_top.show()




















if __name__ == "__main__":
    main()
