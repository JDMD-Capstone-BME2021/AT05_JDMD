import tkinter as tk
import numpy as np
from src import window_elements as we


class Gui:
    def __init__(self):
        self.input = None
        self.sinogram = None
        self.output = None

        self._root = tk.Tk()
        self._root.title('Radon')

        self._f_options = tk.LabelFrame(self._root, borderwidth=1, relief=tk.SUNKEN, labelanchor='nw', text='Options')
        self._f_options.grid(row=0, column=0)

        self._nsamples = we.IntField(self._f_options, 'Number of samples')
        self._start_angle = we.FloatField(self._f_options, 'Start angle', 0)
        self._end_angle = we.FloatField(self._f_options, 'End angle', 180.)

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

    def nsamples(self):
        return self._nsamples.get()

    def method(self):
        return self._method.get()

    def start_angle(self):
        return self._start_angle.get()

    def end_angle(self):
        return self._end_angle.get()

    def src_dir(self):
        return self._intput_dir.get()

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
