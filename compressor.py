import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from tqdm import tqdm

from node import QuadtreeNode

DEFAULT_THRESHOLD = 60


class QuadtreeCompressor:
    def __init__(self, path: str, threshold: int = 20):
        self.path = path
        self.threshold = threshold
        self.image = Image.open(path).convert("RGB")
        self.pixels = np.asarray(self.image, dtype=np.int16)

    def is_uniform(self, x: int, y: int, width: int, height: int) -> bool:
        region = self.pixels[y:y + height, x:x + width]
        base_color = self.pixels[y, x]
        differences = np.abs(region - base_color).sum(axis=2)
        return int(differences.max()) <= self.threshold

    def split_regions(self, x: int, y: int, width: int, height: int):
        w1, w2 = width // 2, width - width // 2
        h1, h2 = height // 2, height - height // 2

        return (
            (x, y, w1, h1),                  # top left
            (x + w1, y, w2, h1),             # top right
            (x, y + h1, w1, h2),             # bottom left
            (x + w1, y + h1, w2, h2),        # bottom right
        )

    def build_tree(
        self,
        x=0,
        y=0,
        width=None,
        height=None,
        progress_bar=None,
    ) -> QuadtreeNode:
        if width is None:
            width = self.image.width
        if height is None:
            height = self.image.height

        if self.is_uniform(x, y, width, height) or width == 1 or height == 1:
            color = self.average_color(x, y, width, height)
            if progress_bar is not None:
                progress_bar.update(width * height)
            return QuadtreeNode(x, y, width, height, color=color)

        children = tuple(
            self.build_tree(child_x, child_y, child_w, child_h, progress_bar)
            for child_x, child_y, child_w, child_h in self.split_regions(x, y, width, height)
        )
        return QuadtreeNode(x, y, width, height, children=children)

    def average_color(self, x: int, y: int, width: int, height: int) -> tuple[int, int, int]:
        region = self.pixels[y:y + height, x:x + width]
        average = region.mean(axis=(0, 1)).astype(int)
        return tuple(int(channel) for channel in average)

    def compress(self) -> QuadtreeNode:
        total_pixels = self.image.width * self.image.height
        with tqdm(total=total_pixels, desc="Compressing", unit="px", unit_scale=True) as progress:
            return self.build_tree(
                x=0,
                y=0,
                width=self.image.width,
                height=self.image.height,
                progress_bar=progress,
            )

    def save(self, output_path: str) -> None:
        root = self.compress()
        data = root.to_dict()

        with open(output_path, "w") as file:
            json.dump(data, file)


class ImageCodec:
    @staticmethod
    def compress(
        input_path: str,
        output_path: str,
        threshold: int = 20,
    ) -> None:
        compressor = QuadtreeCompressor(input_path, threshold)
        compressor.save(output_path)

    @staticmethod
    def decompress(input_path: str, output_path: str) -> None:
        with open(input_path, "r") as file:
            data = json.load(file)

        root = QuadtreeNode.from_dict(data)
        img = Image.new("RGB", (root.width, root.height))
        ImageCodec._draw_node(img, root)
        img.save(output_path)

    @staticmethod
    def _draw_node(img: Image.Image, node: QuadtreeNode) -> None:
        draw = ImageDraw.Draw(img)
        ImageCodec._draw_node_with_draw(draw, node)

    @staticmethod
    def _draw_node_with_draw(draw: ImageDraw.ImageDraw, node: QuadtreeNode) -> None:
        if node.is_leaf():
            draw.rectangle(
                [
                    node.x,
                    node.y,
                    node.x + node.width - 1,
                    node.y + node.height - 1,
                ],
                fill=node.color,
            )
            return
        for child in node.children:
            ImageCodec._draw_node_with_draw(draw, child)


def output_paths(input_path: str) -> tuple[str, str]:
    image_path = Path(input_path)
    compressed_path = image_path.with_name(f"{image_path.stem}_compressed.json")
    decompressed_path = image_path.with_name(f"{image_path.stem}_decompressed{image_path.suffix}")
    return str(compressed_path), str(decompressed_path)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python compressor.py path/to/image")

    input_path = sys.argv[1]
    compressed_path, decompressed_path = output_paths(input_path)

    ImageCodec.compress(input_path, compressed_path, threshold=DEFAULT_THRESHOLD)
    ImageCodec.decompress(compressed_path, decompressed_path)
    print(f"Compressed {input_path} to {compressed_path}")
    print(f"Decompressed {compressed_path} to {decompressed_path}")


if __name__ == "__main__":
    main()
