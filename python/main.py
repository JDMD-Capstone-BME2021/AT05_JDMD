from concurrent.futures import ThreadPoolExecutor
from threading import Event

from session import Session

from gui_window import Gui, s_reconstruct, s_load_images

import logging.config
from pathlib import Path

BASEDIR = Path()
log_config = BASEDIR / 'logging.conf'
logging.config.fileConfig(log_config, disable_existing_loggers=False)
logger = logging.getLogger('app')
logger.info('Logger initiated')

executor = ThreadPoolExecutor(4)
logger.info('Thread pool executor initiated')

active_session = Session()
logger.info('Session created')

e_gui_exited = Event()


def start_gui():
    window = Gui()
    window.run()
    e_gui_exited.set()


@active_session.s_error.connect
def on_session_error(sender, **kwargs):
    logger.error(kwargs['message'])


@s_load_images.connect
def on_load_images(sender, **kwargs):
    logger.info('Loading images...')
    executor.submit(active_session.load_images, kwargs)


@active_session.s_image_loadad.connect
def on_images_loaded(sender):
    logger.info('Images loaded')
    logger.info('Constructing sinogram...')
    executor.submit(active_session.make_sinogram)


@active_session.s_sinogram_constructed.connect
def on_sinogram_constructed(sender):
    logger.info('Sinogram constructed')


@s_reconstruct.connect
def on_reconstruct(sender, **kwargs):
    logger.info('Reconstructing image...')
    executor.submit(active_session.reconstruct, kwargs)


@active_session.s_reconstructed.connect
def on_reconstructed(sender):
    logger.info('Image reconstructed')


logger.info('Starting GUI...')
executor.submit(start_gui)

e_gui_exited.wait()
logger.info('Quitting...')
executor.shutdown()
