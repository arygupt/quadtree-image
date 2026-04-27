# image processing 
import numpy as np
from PIL import Image


FILE_PATH = 'penguins.jpg'


class QuadtreeNode:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: tuple[int, int, int] | None = None,
        children: tuple["QuadtreeNode", "QuadtreeNode", "QuadtreeNode", "QuadtreeNode"] | None = None,
    ):
        ...

    def is_leaf(self) -> bool:
        ...

    def to_dict(self) -> dict:
        ...

    @classmethod
    def from_dict(cls, data: dict) -> "QuadtreeNode":
        ...



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

    def split_regions(self, x, y, width, height):
        w1, w2 = width // 2, width - width // 2
        h1, h2 = height // 2, height - height // 2
        return (
            (x, y, w1, h1),                  # topleft
            (x + w1, y, w2, h1),             # topright
            (x, y + h1, w1, h2),             # bottom left
            (x + w1, y + h1, w2, h2),        # bottom right
        )
    def build_tree(self, x=0, y=0, width=None, height=None):
        if width is None:
            width = self.image.width
        if height is None:
            height = self.image.height
        if self.is_uniform(x, y, width, height) or width == 1 or height == 1:
            color = self.average_color(x, y, width, height)
            return QuadtreeNode(x, y, width, height, color=color)
        children = tuple(
            self.build_tree(child_x, child_y, child_w, child_h)
            for child_x, child_y, child_w, child_h in self.split_regions(x, y, width, height)
        )
        return QuadtreeNode(x, y, width, height, children=children)


"""
class QuadtreeCompressor:
    def __init__(self, path: str, threshold: int = 20):
        ...

    def is_uniform(self, x: int, y: int, width: int, height: int) -> bool:
        ...

    def average_color(self, x: int, y: int, width: int, height: int) -> tuple[int, int, int]:
        ...

    def build_tree(
        self,
        x: int = 0,
        y: int = 0,
        width: int | None = None,
        height: int | None = None,
    ) -> QuadtreeNode:
        ...

    def compress(self) -> QuadtreeNode:
        ...

    def save(self, output_path: str) -> None:
        ...
"""


class ImageCodec:
    @staticmethod
    def compress(input_path: str, output_path: str, threshold: int = 20) -> None:
        ...

    @staticmethod
    def decompress(input_path: str, output_path: str) -> None:
        ...

    
    
    
def main():
    QDT = QuadtreeCompressor(FILE_PATH)
    




















if __name__ == "__main__":
    main()
