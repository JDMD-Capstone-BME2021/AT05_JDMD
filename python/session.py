from reconstruction import core
from blinker import Signal
from PIL import Image
from array2gif import write_gif
import numpy as np


class Session:
    def __init__(self):
        self.load_options: dict = {}
        self.reconstruction_options: dict = {}
        self.images = None
        self.sinogram = None
        self.reconstruction = None
        self.is_images_loaded = False
        self.is_sinogram_constructed = False
        self.is_reconstructed = False
        self.s_image_loadad = Signal()
        self.s_sinogram_constructed = Signal()
        self.s_reconstructed = Signal()
        self.s_error = Signal()
        pass

    def load_images(self, load_options: dict):
        self.load_options = load_options
        # todo: verify data
        if 'input_dir' not in self.load_options:
            quit(1)
        self.images, _, _ = core.load_images(**self.load_options)
        self.is_images_loaded = True
        self.s_image_loadad.send()

    def make_sinogram(self):
        if not self.is_images_loaded:
            self.s_error.send(message='Attempted making sinogram without images loaded')
        self.sinogram = core.make_sinogram(self.images)
        self.is_sinogram_constructed = True
        self.s_sinogram_constructed.send()

    def reconstruct(self, reconstruction_options):
        self.reconstruction_options = reconstruction_options
        self.reconstruction = core.reconstruct(self.sinogram, **self.reconstruction_options)
        self.is_reconstructed = True
        self.s_reconstructed.send()

    def save_session(self, filepath):
        print('trying to save inputs')
        np.save('data.npy', self.images)
        print('trying to save as image')
        im = Image.fromarray(self.images[:, :, 100])
        im.show()
        # im.save('data.png', 'PNG')
        print('inputs saved')
        # pass
