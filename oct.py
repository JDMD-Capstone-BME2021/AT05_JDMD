import numpy as np
from PIL import Image, ImageOps
from pathlib import Path
import threading
from skimage.transform import rescale, iradon, iradon_sart


def _make_square(im, minsize=256, fill_color=(255, 255, 255, 0)):
    x, y = im.size
    size = max(minsize, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im


def prepare_img(img_path, resolution=256, padding=0.3):
    src = Image.open(img_path)
    img = _make_square(src, minsize=int(src.size[0] * (1 + padding)))
    img = ImageOps.grayscale(img)
    img = ImageOps.invert(img)
    img = rescale(np.asarray(img), scale=resolution / img.size[0], multichannel=False, anti_aliasing=True)
    return img


def load_images(dir_path, resolution=256, padding=0.3):
    files = [x for x in Path(dir_path).rglob('*')]
    n = len(files)
    images = np.zeros((resolution, resolution, n))
    for i in range(n):
        print('Reading ' + str(files[i]) + '\n')
        images[:, :, i] = prepare_img(files[i], resolution=resolution, padding=padding)
    print('Finished reading images\n')
    return images


def make_sinogram(images):
    print('Constructing sinogram\n')
    sinogram = np.zeros(images.shape)
    for i in range(sinogram.shape[0]):
        sinogram[i, :, :] = np.squeeze(images[i, :, :])
    print('Sinogram construction complete')


def reconstruct_fbp(sinogram, nthreads=1, method='fbp', **kwargs):
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
