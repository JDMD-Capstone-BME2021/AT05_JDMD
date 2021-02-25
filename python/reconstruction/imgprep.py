from PIL import Image, ImageOps
from pathlib import Path
from skimage.transform import rescale
import numpy as np


def _make_square(im: Image, minsize: int = 256, fill_color: tuple = (255, 255, 255, 0)) -> Image:
    """
    Creates a sqaure image of the specified size with other image pasted in center
    :param im: image to paste
    :param minsize: minimum image size
    :param fill_color: image fill color
    :return: PIL image
    """
    x, y = im.size
    size = max(minsize, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im


def load_img(img_path: Path) -> np.array:
    """
    Load an image from Path
    """
    src = Image.open(img_path)
    return src


def prepare_img(src, resolution: int = 256, padding: float = 0.3) -> (np.array, np.array, np.array):
    """
    Preprocesses the image -- makes it square, converts to greyscale, inverts, adds padding and rescales
    :param src: image
    :param resolution: final resolution of the image
    :param padding: padding fraction
    :return: processed image as a np.array
    """
    img = _make_square(src, minsize=int(src.size[0] * (1 + padding)))
    r, g, b, _ = img.split()
    r, g, b = np.asarray(r), np.asarray(g), np.asarray(b)
    scale = resolution / r.shape[0]
    r = rescale(r, scale=scale, multichannel=False, anti_aliasing=True)
    g = rescale(g, scale=scale, multichannel=False, anti_aliasing=True)
    b = rescale(b, scale=scale, multichannel=False, anti_aliasing=True)
    # img = ImageOps.grayscale(img)
    # img = ImageOps.invert(img)
    return r, g, b
