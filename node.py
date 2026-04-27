
from compressor import *


FILE_PATH = 'penguins.jpg'


class QuadtreeNode:
    def __init__(self, x, y, width, height, color = None,children = None):
        self.x = x;
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.children = children; # tuple with 4 quadTree nodes

    def is_leaf(self) -> bool:
        if(self.color != None and self.children == None):
            return True
        return False

    def to_dict(self) -> dict:
        if self.is_leaf():
            return {
                "x": self.x,
                "y": self.y,
                "width": self.width,
                "height": self.height,
                "color": list(self.color),
                "children": None
            }
        else:
            return {
                "x": self.x,
                "y": self.y,
                "width": self.width,
                "height": self.height,
                "color": None,
                "children": [
                    child.to_dict()
                    for child in self.children
                ]
            }

    @classmethod
    def from_dict(cls, data: dict) -> "QuadtreeNode":
            if (data["children"] is None):
                return cls (
                    x = data["x"],
                    y = data["y"],
                    width = data["width"],
                    height = data["height"],
                    color=tuple(data["color"]),
                    children = None
                )
            children_list = []        

            for child_data in data["children"]:
                node = cls.from_dict(child_data)
                children_list.append(node)
             
            structuredChildren = tuple(children_list)

            return cls (
                    x = data["x"],
                    y = data["y"],
                    width = data["width"],
                    height = data["height"],
                    color=None,
                    children = structuredChildren 
            )