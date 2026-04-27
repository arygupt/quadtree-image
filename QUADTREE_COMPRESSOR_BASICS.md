# Basics of Building a Quadtree Image Compressor

## What a Quadtree Is

A quadtree is a tree where each parent node can have four children. For image compression, each node represents a rectangular region of the image.

If a region is simple enough, the node stores one color for the whole region. If the region has too much color variation, the region gets split into four smaller regions:

- top-left
- top-right
- bottom-left
- bottom-right

This repeats recursively until each region is simple enough to represent with one color, or until the region is only one pixel wide or tall.

## The Main Idea

The compressor starts with the whole image:

```text
(0, 0, image_width, image_height)
```

Then it asks:

```text
Is this region uniform enough?
```

If yes, store a leaf node with an average color.

If no, split the region into four smaller regions and repeat the same process on each one.

## Important Classes

### `QuadtreeNode`

This class stores one rectangle of the image.

A node should usually store:

```python
x: int
y: int
width: int
height: int
color: tuple[int, int, int] | None
children: tuple[QuadtreeNode, QuadtreeNode, QuadtreeNode, QuadtreeNode] | None
```

If `color` exists and `children` is `None`, the node is a leaf.

If `children` exists, the node is an internal node that points to four smaller regions.

Useful methods:

```python
def is_leaf(self) -> bool:
    ...

def to_dict(self) -> dict:
    ...

@classmethod
def from_dict(cls, data: dict) -> "QuadtreeNode":
    ...
```

`to_dict()` and `from_dict()` are helpful because you can save the compressed tree as JSON.

## Compressor Methods

### `is_uniform()`

This method checks whether a region is simple enough to store as one color.

Basic idea:

```python
def is_uniform(self, x, y, width, height):
    ...
```

It loops through the pixels inside the rectangle and compares them to a reference color. If the difference is larger than your threshold, the region is not uniform.

The threshold controls compression quality:

- lower threshold means more detail and less compression
- higher threshold means less detail and more compression

### `average_color()`

This method calculates the average RGB color of a region.

Basic idea:

```python
def average_color(self, x, y, width, height):
    ...
```

It should:

1. Loop through every pixel in the region.
2. Add up all red, green, and blue values.
3. Divide each total by the number of pixels.
4. Return the average as `(r, g, b)`.

Example return value:

```python
(128, 104, 92)
```

### `split_regions()`

This method should only handle geometry. It should not decide whether to compress or recurse.

It takes one rectangle and returns four smaller rectangles:

```python
def split_regions(self, x, y, width, height):
    w1, w2 = width // 2, width - width // 2
    h1, h2 = height // 2, height - height // 2

    return (
        (x, y, w1, h1),
        (x + w1, y, w2, h1),
        (x, y + h1, w1, h2),
        (x + w1, y + h1, w2, h2),
    )
```

This returns coordinates, not cropped images. That is important because the quadtree needs to remember where each region belongs in the original image.

### `build_tree()`

This is the main recursive compression method.

Basic idea:

```python
def build_tree(self, x=0, y=0, width=None, height=None):
    ...
```

The method should:

1. Default to the whole image if no region is given.
2. Check whether the current region is uniform.
3. If it is uniform, return a `QuadtreeNode` with a color.
4. If it is not uniform, call `split_regions()`.
5. Recursively call `build_tree()` on each child region.
6. Return a parent `QuadtreeNode` with four children.

Example structure:

```python
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
```

## How Compression Works

Compression is mostly this:

```python
root = compressor.build_tree()
```

The root node represents the entire image. Every child node represents a smaller rectangle.

Then you save the root node:

```python
data = root.to_dict()
```

After converting the tree to a dictionary, you can save it as JSON.

## How Decompression Works

Decompression does the opposite.

It should:

1. Load the saved tree.
2. Create a blank image with the original width and height.
3. Walk through the tree.
4. For every leaf node, fill that node's rectangle with its stored color.
5. Save the rebuilt image.

The basic render logic looks like:

```python
def render_node(image, node):
    if node.is_leaf():
        fill_rectangle(image, node.x, node.y, node.width, node.height, node.color)
        return

    for child in node.children:
        render_node(image, child)
```

## Recommended Build Order

Build the project in this order:

1. Finish `QuadtreeNode.__init__()`.
2. Finish `QuadtreeNode.is_leaf()`.
3. Finish `average_color()`.
4. Make sure `split_regions()` returns four coordinate tuples.
5. Finish `build_tree()`.
6. Add `to_dict()` and `from_dict()`.
7. Add saving and loading with `json`.
8. Add decompression by drawing leaf nodes back onto a blank image.

## Mental Model

Use this rule:

```text
split_regions() = where to split
build_tree() = whether to split and how to recurse
```

`split_regions()` should not build nodes.

`build_tree()` should use `split_regions()` to build nodes recursively.

## Common Mistakes

- Returning cropped images from `split_regions()` instead of coordinates.
- Forgetting the base case in `build_tree()`.
- Splitting forever when width or height reaches `1`.
- Not storing `x` and `y`, which makes decompression harder.
- Saving only colors without saving the tree structure.
- Having duplicate class definitions with the same name.

## Minimal Method List

For a working version, you probably want these methods:

```python
class QuadtreeNode:
    def __init__(self, x, y, width, height, color=None, children=None):
        ...

    def is_leaf(self):
        ...

    def to_dict(self):
        ...

    @classmethod
    def from_dict(cls, data):
        ...


class QuadtreeCompressor:
    def __init__(self, path, threshold=20):
        ...

    def is_uniform(self, x, y, width, height):
        ...

    def average_color(self, x, y, width, height):
        ...

    def split_regions(self, x, y, width, height):
        ...

    def build_tree(self, x=0, y=0, width=None, height=None):
        ...

    def save(self, output_path):
        ...
```

