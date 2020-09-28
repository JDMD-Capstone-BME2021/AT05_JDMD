import tkinter as tk
import numpy as np
import oct
from src import window_elements as we


class Gui:
    def __init__(self):
        self.input = None
        self.sinogram = None
        self.reconstructed = None

        self._root = tk.Tk()
        self._root.title('Radon')

        self._f_options = tk.LabelFrame(self._root, borderwidth=1, relief=tk.SUNKEN, labelanchor='nw', text='Options')
        self._f_options.grid(row=0, column=0)

        self._resolution = we.IntField(self._f_options, 'Resolution', 256)
        self._padding = we.FloatField(self._f_options, 'Padding', 0.3)
        self._start_angle = we.FloatField(self._f_options, 'Start angle', 0)
        self._end_angle = we.FloatField(self._f_options, 'End angle', 180.)
        self._nthreads = we.IntField(self._f_options, 'Threads', 4)

        self._method = we.RadioMenu(self._f_options)
        self._method.add_option('FBP', 0, 0, 0)
        self._method.add_option('SART', 1, 0, 1)

        self._f_method_options = tk.LabelFrame(self._f_options, borderwidth=1, labelanchor='nw')
        self._f_method_options.pack(fill=tk.X, expand=True)
        self._method.add_observer(self.__method_observer)

        self._fbp_pack = we.ManagedPack()
        self._fbp_filter = we.Dropdown(self._f_method_options, 'Filter',
                                       ['Ramp', 'Shepp-Logan', 'Cosine', 'Hamming', 'Hann', 'None'], False)
        self._fbp_pack.add(self._fbp_filter, fill=tk.X, expand=True)
        self._fbp_interpolation = we.Dropdown(self._f_method_options, 'Interpolation', ['Linear', 'Nearest', 'Cubic'],
                                              False)
        self._fbp_pack.add(self._fbp_interpolation, fill=tk.X, expand=True)

        self._sart_pack = we.ManagedPack()
        self._sart_iterations = we.IntField(self._f_method_options, 'Iterations', 1, False)
        self._sart_pack.add(self._sart_iterations, fill=tk.X, expand=True)
        self._sart_relaxation = we.FloatField(self._f_method_options, 'Relaxation', 0.15, False)
        self._sart_pack.add(self._sart_relaxation, fill=tk.X, expand=True)

        self._intput_dir = we.DirBrowser(t_master=self._f_options, t_max_len=16)

        self._f_save = tk.LabelFrame(self._root)
        self._f_save.grid(row=1, column=0)

        options = {'filetypes': [('Numpy array', '.npy'), ('Comma-separated values', '.csv')],
                   'initialfile': 'input.npy'}
        self._save_input = we.SaveAs(master=self._f_save, text='Save input', file_options=options,
                                     save_fcn=self.save_input)
        self._save_input.pack(side=tk.LEFT)

        options['initialfile'] = 'sinogram.npy'
        self._save_input = we.SaveAs(master=self._f_save, text='Save sinogram', file_options=options,
                                     save_fcn=self.save_sinogram)
        self._save_input.pack(side=tk.LEFT)

        options['initialfile'] = 'roconstruction.npy'
        self._save_input = we.SaveAs(master=self._f_save, text='Save reconstruction', file_options=options,
                                     save_fcn=self.save_reconstructed)
        self._save_input.pack(side=tk.LEFT)

    @staticmethod
    def save_numpy(name, arr):
        ext = name[-3:-1]
        if ext == 'npy':
            np.save(name, arr)
        elif ext == 'csv':
            np.savetxt(name, arr, delimiter=',')

    def save_input(self, name):
        if self.input is None:
            print('Input is not processes\n')
            return
        self.save_numpy(name, self.input)

    def save_sinogram(self, name):
        if self.input is None:
            print('Sinogram is not processed\n')
            return
        self.save_numpy(name, self.sinogram)

    def save_reconstructed(self, name):
        if self.input is None:
            print('Reconstruction is not processed\n')
            return
        self.save_numpy(name, self.input)

    def process(self):
        # freezing parameters
        input_dir = self.input_dir
        resolution = self.resolution
        padding = self.padding
        method = self.method
        nthreads = self.nthreads
        start_angle = self.start_angle
        end_angle = self.end_angle

        # loading images
        self.input = oct.load_images(input_dir, resolution=resolution, padding=padding)

        # constructing sinogram
        self.sinogram = oct.make_sinogram(self.input)

        # calculating reconstruction parameters
        nsamples = self.input.shape[2]
        theta = np.linspace(start_angle, end_angle, nsamples, endpoint=False)
        reconstruction_opt = {'theta': theta}

        # reconstructing image
        self.reconstructed = oct.reconstruct(self.sinogram, nthreads=nthreads, method=method, **reconstruction_opt)

    @property
    def method(self):
        if self._method.get() == 0:
            return 'fbp'
        return 'sart'

    @property
    def fbp_filter(self):
        a = self._fbp_filter.get()
        if a == 0:
            return 'ramp'
        elif a == 1:
            return 'shepp-logan'
        elif a == 2:
            return 'cosine'
        elif a == 3:
            return 'hamming'
        elif a == 4:
            return 'hann'
        return None

    @property
    def fbp_interpolation(self):
        a = self._fbp_interpolation.get()
        if a == 0:
            return 'linear'
        if a == 1:
            return 'nearest'
        if a == 2:
            return 'cubic'

    @property
    def sart_iterations(self):
        return self._sart_iterations.get()

    @property
    def sart_relaxation(self):
        return self._sart_relaxation.get()

    @property
    def start_angle(self):
        return self._start_angle.get()

    @property
    def end_angle(self):
        return self._end_angle.get()

    @property
    def input_dir(self):
        return self._intput_dir.get()

    @property
    def resolution(self):
        return self._resolution.get()

    @property
    def padding(self):
        return self._padding.get()

    @property
    def nthreads(self):
        return self._nthreads.get()

    def run(self):
        self._root.mainloop()

    def __method_observer(self, *args):
        if self._method.get() == 0:
            self._f_method_options.config(text='FBP')
            self._sart_pack.pack_forget()
            self._fbp_pack.pack()
        else:
            self._f_method_options.config(text='SART')
            self._fbp_pack.pack_forget()
            self._sart_pack.pack()
