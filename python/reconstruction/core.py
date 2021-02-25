import python.reconstruction.imgprep as imgprep
from python.reconstruction.structs import ReconstructionOptions

from pathlib import Path
from skimage.transform import iradon, iradon_sart
import numpy as np
import threading


def load_images(input_dir: str, resolution: int = 256, padding: float = 0.3) -> (np.array, np.array, np.array):
    """
    Loads images from specified directory and preprocesses them:

    - makes it square

    - converts to greyscale & inverts it

    - adds padding

    - rescales it

    :param input_dir: directory to load images from
    :param resolution: final image resolution
    :param padding: padding fraction
    :return: array of images, with image index in position 2
    """
    files = [x for x in Path(input_dir).rglob('*')]
    n = len(files)
    # images = np.zeros((resolution, resolution, n))
    r_img = np.zeros((resolution, resolution, n))
    g_img = np.zeros((resolution, resolution, n))
    b_img = np.zeros((resolution, resolution, n))
    for i in range(n):
        print('Reading ' + str(files[i]) + '\n')
        r, g, b = imgprep.prepare_img(imgprep.load_img(files[i]), resolution=resolution, padding=padding)
        # images[:, :, i] = r
        r_img[:, :, i] = r
        g_img[:, :, i] = g
        b_img[:, :, i] = b

    return r_img, g_img, b_img


def make_sinogram(images: np.array) -> np.array:
    """
    Makes a sinogram from an image array
    :param images: image array with image index in position 2
    :return: array of sinogram with sinogram index in position 0
    """
    sinogram = np.zeros(images.shape)
    for i in range(sinogram.shape[0]):
        sinogram[i, :, :] = np.squeeze(images[i, :, :])
    return sinogram


def _reconstruct(sinogram: np.array, nthreads: int = 1, method: str = 'fbp', **kwargs) -> np.array:
    """
    Reconstructs tomographic images from a sinogram array
    :param sinogram: sinogram array, indexed at position 0
    :param nthreads: number of threads
    :param method: reconstruction method -- 'fbp' (filtered back projection) or 'sart' simultaneous reconstruction
    :param kwargs: arguments forwarded to reconstuction method
    :return: tomographic image todo: add specification to axes
    """
    print('Reconstructing image with parameters:'
          '\n\tsize: {0}\n\tnthreads: {1}\n\tmethod: {2}'.format(sinogram.shape[0], nthreads, method))
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


def reconstruct(sinogram, opts: ReconstructionOptions) -> np.array:
    nsamples = sinogram.shape[2]
    theta = np.linspace(opts.start_angle, opts.end_angle, nsamples, endpoint=False)
    reconstruction_opt = {'theta': theta}
    if opts.method == 'fbp':
        reconstruction_opt['filter'] = opts.fbp_filter
        reconstruction_opt['interpolation'] = opts.fbp_interpolation
    elif opts.method == 'sart':
        reconstruction_opt['relaxation'] = opts.sart_relaxation

    reconstructed = _reconstruct(sinogram, nthreads=opts.nthreads, method=opts.method, **reconstruction_opt)

    # additional iterations for SART
    if opts.method == 'sart' and opts.sart_iterations > 1:
        for i in range(1, opts.sart_iterations):
            print('SART iteration ' + str(i + 1))
            reconstruction_opt['image'] = reconstructed
            reconstructed = _reconstruct(sinogram, nthreads=opts.nthreads, method=opts.method, **reconstruction_opt)

    return reconstructed
