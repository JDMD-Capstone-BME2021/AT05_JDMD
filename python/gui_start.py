# Threading
from concurrent.futures import ThreadPoolExecutor
from threading import Event
# GUI
from gui_window import Gui
# Background functions
from reconstruction import core
from reconstruction.events import ReconstructionEvent, LoadimagesEvent

# Utilities
import logging.config
import argparse
from pathlib import Path

BASEDIR = Path()  # current working directory, must contain logging.conf

# configure logger
log_config = BASEDIR / 'logging.conf'
logging.config.fileConfig(log_config, disable_existing_loggers=False)
logger = logging.getLogger('app')
logger.info('Session started')
# todo use json logger
# https://www.datadoghq.com/blog/python-logging-best-practices/
# https://libraries.io/pypi/python-json-logger

nthreads = 4
update_interval = 1 / 100

e_gui_exited = Event()
e_reset = Event()
e_load_images = LoadimagesEvent()
e_start_reconstruction = ReconstructionEvent()

images = None
sinogram = None
reconstruction = None


def start_gui():
    window = Gui()
    window.e_load_images = e_load_images
    window.e_start_reconstruction = e_start_reconstruction
    window.run()
    logger.info('GUI exited')
    e_gui_exited.set()


def load_images():
    # global lock
    # with lock:
    e_load_images.wait()
    opts = e_load_images.load_options
    e_load_images.clear()
    ims = core.load_images(opts.input_dir, opts.resolution, opts.padding)
    return ims


def on_load_images_complete(future):
    # global lock
    global images, sinogram
    # with lock:
    images = future.result()
    logger.info('Image loading complete. Constructing sinogram...')
    sinogram = core.make_sinogram(images)
    logger.info('Sinogram construction complete')
    logger.info('You can now run image reconstruction')


def reconstruct():
    opts = e_start_reconstruction.reconstruction_options
    e_start_reconstruction.clear()
    return core.reconstruct(sinogram, opts)


def on_reconstruct_complete(future):
    global reconstruction
    reconstruction = future.result()
    logger.info('Image reconstruction complete')
    logger.info('Output shape: ', reconstruction.shape)


logger.info('Starting GUI')

executor = ThreadPoolExecutor(nthreads)
logger.info('Number of threads allocated: ' + str(nthreads))

logger.info('Starting GUI...')
gui_thread = executor.submit(start_gui)

while not e_gui_exited.is_set():
    e_load_images.wait(update_interval)
    if e_load_images.is_set():
        im_load_thread = executor.submit(load_images)
        im_load_thread.add_done_callback(on_load_images_complete)

    e_start_reconstruction.wait(update_interval)
    if e_start_reconstruction.is_set():
        im_reconstruction_thread = executor.submit(reconstruct)
        im_reconstruction_thread.add_done_callback(on_reconstruct_complete)

e_gui_exited.wait()

logger.info('Quitting...')
quit()
