from gui_window import Gui
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from reconstruction.events import ReconstructionEvent, LoadimagesEvent
from reconstruction import core
import matplotlib.pyplot as plt

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
    print('GUI exited')
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
    print('Image loading complete. Constructing sinogram...')
    sinogram = core.make_sinogram(images)
    print('Sinogram construction complete')
    print('You can now run image reconstruction')


def reconstruct():
    opts = e_start_reconstruction.reconstruction_options
    e_start_reconstruction.clear()
    return core.reconstruct(sinogram, opts)


def on_reconstruct_complete(future):
    global reconstruction
    reconstruction = future.result()
    print('Image reconstruction complete')
    print('Output shape: ', reconstruction.shape)


print('Starting up...')

executor = ThreadPoolExecutor(nthreads)
print('Number of threads allocated: ' + str(nthreads))

print('Starting GUI...')
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

print('Quitting...')
quit()
