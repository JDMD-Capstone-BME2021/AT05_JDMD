import numpy as np
from PIL import Image, ImageOps
from pathlib import Path
import threading
from skimage.transform import rescale, iradon, iradon_sart


def _make_square(im: Image, minsize: int = 256, fill_color: tuple = (255, 255, 255, 0)) -> np.array:
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


def _prepare_img(img_path: Path, resolution: int = 256, padding: float = 0.3) -> np.array:
    """
Preprocesses the image -- loads it, makes it square, converts to greyscale, inverts, adds padding and rescales
    :param img_path: path to the image to load
    :param resolution: final resolution of the image
    :param padding: padding fraction
    :return: processed image as a np.array
    """
    src = Image.open(img_path)
    img = _make_square(src, minsize=int(src.size[0] * (1 + padding)))
    img = ImageOps.grayscale(img)
    img = ImageOps.invert(img)
    img = rescale(np.asarray(img), scale=resolution / img.size[0], multichannel=False, anti_aliasing=True)
    return img


def load_images(dir_path: str, resolution: int = 256, padding: float = 0.3) -> np.array:
    """
Loads images from specified directory and preprocesses them:

- makes it square

- converts to greyscale & inverts it

- adds padding

- rescales it

    :param dir_path: directory to load images from
    :param resolution: final image resolution
    :param padding: padding fraction
    :return: array of images, with image index in position 2
    """
    files = [x for x in Path(dir_path).rglob('*')]
    n = len(files)
    images = np.zeros((resolution, resolution, n))
    for i in range(n):
        print('Reading ' + str(files[i]) + '\n')
        images[:, :, i] = _prepare_img(files[i], resolution=resolution, padding=padding)
    print('Finished reading images\n')
    return images


def make_sinogram(images: np.array) -> np.array:
    """
Makes a sinogram from an image array
    :param images: image array with image index in position 2
    :return: array of sinogram with sinogram index in position 0
    """
    print('Constructing sinogram\n')
    sinogram = np.zeros(images.shape)
    for i in range(sinogram.shape[0]):
        sinogram[i, :, :] = np.squeeze(images[i, :, :])
    print('Sinogram construction complete')
    return sinogram


def reconstruct(sinogram: np.array, nthreads: int = 1, method: str = 'fbp', **kwargs) -> np.array:
    """
Reconstructs tomographic images from a sinogram array
    :param sinogram: sinogram array, indexed at position 0
    :param nthreads: number of threads
    :param method: reconstruction method -- 'fbp' (filtered back projection) or 'sart' simultaneous reconstruction
    :param kwargs: arguments forwarded to reconstuction method
    :return: tomographic image todo: add specification to axes
    """
    reconstructed = np.zeros((sinogram.shape[0], sinogram.shape[0], sinogram.shape[0]))
    lock = threading.Lock()

    if method == 'fbp':
        __iradon = iradon
    elif method == 'sart':
        __iradon = iradon_sart

    def __reconstruct(start, step):
        for j in range(start, sinogram.shape[0], step):
            tmp = __iradon(sinogram[j, :, :], **kwargs)
            lock.acquire()
            reconstructed[:, :, j] = tmp
            lock.release()

    threads = []
    for i in range(nthreads):
        threads.append(threading.Thread(target=__reconstruct, args=(i, nthreads)))

    for i in range(nthreads):
        threads[i].start()

    for i in range(nthreads):
        threads[i].join()

    return reconstructed
