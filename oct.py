import numpy as np
from PIL import Image, ImageOps
from pathlib import Path
import threading
from skimage.transform import rescale, iradon, iradon_sart


def _make_square(im: Image, minsize: int = 256, fill_color: tuple = (255, 255, 255, 0)) -> np.array:
    x, y = im.size
    size = max(minsize, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im


def _prepare_img(img_path: Path, resolution: int = 256, padding: float = 0.3) -> np.array:
    src = Image.open(img_path)
    img = _make_square(src, minsize=int(src.size[0] * (1 + padding)))
    img = ImageOps.grayscale(img)
    img = ImageOps.invert(img)
    img = rescale(np.asarray(img), scale=resolution / img.size[0], multichannel=False, anti_aliasing=True)
    return img


def load_images(dir_path: str, resolution: int = 256, padding: float = 0.3) -> np.array:
    files = [x for x in Path(dir_path).rglob('*')]
    n = len(files)
    images = np.zeros((resolution, resolution, n))
    for i in range(n):
        print('Reading ' + str(files[i]) + '\n')
        images[:, :, i] = _prepare_img(files[i], resolution=resolution, padding=padding)
    print('Finished reading images\n')
    return images


def make_sinogram(images: np.array) -> np.array:
    print('Constructing sinogram\n')
    sinogram = np.zeros(images.shape)
    for i in range(sinogram.shape[0]):
        sinogram[i, :, :] = np.squeeze(images[i, :, :])
    print('Sinogram construction complete')


def reconstruct_fbp(sinogram: np.array, nthreads: int = 1, method: str = 'fbp', **kwargs) -> np.array:
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
