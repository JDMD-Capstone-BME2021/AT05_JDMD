import gui.window_elements as we
from reconstruction.structs import ReconstructionOptions, ImgLoadOptions

import tkinter as tk
import numpy as np
from PIL import Image

from blinker import Signal
from tkinter import filedialog

s_load_images = Signal()
s_reconstruct = Signal()
s_save_images = Signal()


class Gui:
    def __init__(self):
        self.e_load_images = None
        self.e_start_reconstruction = None

        self._bgcolor = '#d9d9d9'
        self.theme = {'background': self._bgcolor}
        self.btn_opts = {'padx': 2, 'pady': 2}

        self.root = tk.Tk()
        self.root.title('Radon')
        self.root.minsize(800, 600)
        self.root.resizable(1, 1)
        self.root.configure(**self.theme)

        # region Tool bar
        self._tool_bar = tk.Frame(self.root)
        self._tool_bar.configure(**self.theme)
        self._tool_bar.place(relx=0.0, rely=0.0, relheight=0.05, relwidth=1.0)

        # Tool bar -- Save input
        options = {'filetypes': [('Numpy array', '.npy'), ('Comma-separated values', '.csv')],
                   'initialfile': 'input.npy'}
        # self._save_input = we.SaveAs(master=self._tool_bar, text='Save input', file_options=options,
        #                              save_fcn=self.save_input)
        # self._save_input.configure(**self.theme)
        # self._save_input.configure(**self.btn_opts)
        # self._save_input.configure_btn(**self.theme)
        # self._save_input.pack(side=tk.LEFT)

        self._save_sinogram = tk.Button(master=self._tool_bar, text='Save session', command=self.save_input)
        self._save_sinogram.pack(side=tk.LEFT)
        # Tool bar -- Save sinogram
        options['initialfile'] = 'sinogram.npy'
        self._save_sinogram = we.SaveAs(master=self._tool_bar, text='Save sinogram', file_options=options,
                                        save_fcn=self.save_sinogram)
        self._save_sinogram.configure(**self.theme)
        self._save_sinogram.configure(**self.btn_opts)
        self._save_sinogram.configure_btn(**self.theme)
        self._save_sinogram.pack(side=tk.LEFT)

        # Tool bar -- Save reconstruction
        options['initialfile'] = 'reconstruction.npy'
        self._save_reconstruction = we.SaveAs(master=self._tool_bar, text='Save reconstruction', file_options=options,
                                              save_fcn=self.save_reconstruction)
        self._save_reconstruction.configure(**self.theme)
        self._save_reconstruction.configure(**self.btn_opts)
        self._save_reconstruction.configure_btn(**self.theme)
        self._save_reconstruction.pack(side=tk.LEFT)
        # endregion

        # region Work area
        self.work_area = tk.Frame(self.root)
        self.work_area.place(relx=0.0, rely=0.05, relheight=0.95, relwidth=1.0)
        self.work_area.configure(relief='groove')
        self.work_area.configure(borderwidth="2")
        self.work_area.configure(**self.theme)

        # Canvas
        self._preview = we.ImgView(self.work_area)
        # self._preview.update_size()
        self._preview.place(relx=0.3, rely=0.02)
        self._preview.configure(**self.theme)
        self._preview.configure(borderwidth="2")
        self._preview.configure(insertbackground="black")
        self._preview.configure(relief="ridge")
        self._preview.configure(selectbackground="blue")
        self._preview.configure(selectforeground="white")

        # todo: remove placeholder
        img = Image.open('gui/sample.jpg')
        self._preview.set_image(img)

        # region Options
        self._options = tk.LabelFrame(self.work_area)
        self._options.place(relx=0.01, rely=0.01, relheight=0.7, relwidth=0.25)
        self._options.configure(relief='groove')
        self._options.configure(text='Configuration')
        self._options.configure(**self.theme)

        # Options -- Image resolution
        self._resolution = we.IntField(self._options, 'Resolution', 256)
        self._resolution.configure(**self.theme)
        self._resolution.configure_label(**self.theme)
        self._resolution.pack(fill=tk.X, expand=True)
        self._resolution.place(relx=0.01, rely=0.01, relheight=0.06, relwidth=0.98)

        # Options -- Image padding
        self._padding = we.FloatField(self._options, 'Padding', 0.3)
        self._padding.configure(**self.theme)
        self._padding.configure_label(**self.theme)
        self._padding.pack(fill=tk.X, expand=True)
        self._padding.place(relx=0.01, rely=0.07, relheight=0.06, relwidth=0.98)

        # Options -- Start angle
        self._start_angle = we.FloatField(self._options, 'Start angle', 0)
        self._start_angle.configure(**self.theme)
        self._start_angle.configure_label(**self.theme)
        self._start_angle.pack(fill=tk.X, expand=True)
        self._start_angle.place(relx=0.01, rely=0.13, relheight=0.06, relwidth=0.98)

        # Options -- End angle
        self._end_angle = we.FloatField(self._options, 'End angle', 180.)
        self._end_angle.configure(**self.theme)
        self._end_angle.configure_label(**self.theme)
        self._end_angle.pack(fill=tk.X, expand=True)
        self._end_angle.place(relx=0.01, rely=0.19, relheight=0.06, relwidth=0.98)

        # Options -- Number of threads
        self._nthreads = we.IntField(self._options, 'Threads', 4)
        self._nthreads.configure(**self.theme)
        self._nthreads.configure_label(**self.theme)
        self._nthreads.pack(fill=tk.X, expand=True)
        self._nthreads.place(relx=0.01, rely=0.25, relheight=0.06, relwidth=0.98)

        # Options -- Reconstruction method
        self._method = we.RadioMenu(self._options)
        self._method.add_option('FBP', 0, 0, 0)
        self._method.add_option('SART', 1, 0, 1)
        self._method.configure(**self.theme)
        self._method.set_theme(**self.theme)
        self._method.place(relx=0.01, rely=0.31, relheight=0.06, relwidth=0.98)

        # Options -- Advanced reconstruction options
        self._method_options = tk.LabelFrame(self._options, borderwidth=1, labelanchor='nw')
        self._method_options.pack(fill=tk.X, expand=True)
        self._method_options.configure(**self.theme)
        self._method_options.place(relx=0.01, rely=0.37, relwidth=0.98)

        self._fbp_pack = we.ManagedPack()

        self._fbp_filter = we.Dropdown(self._method_options, 'Filter',
                                       ['Ramp', 'Shepp-Logan', 'Cosine', 'Hamming', 'Hann', 'None'])
        self._fbp_filter.configure(**self.theme)
        self._fbp_filter.configure_label(**self.theme)
        self._fbp_filter.configure_combobox(**self.theme)
        self._fbp_pack.add(self._fbp_filter, fill=tk.X, expand=True)

        self._fbp_interpolation = we.Dropdown(self._method_options, 'Interpolation', ['Linear', 'Nearest', 'Cubic'])
        self._fbp_interpolation.configure(**self.theme)
        self._fbp_interpolation.configure_label(**self.theme)
        self._fbp_interpolation.configure_combobox(**self.theme)
        self._fbp_pack.add(self._fbp_interpolation, fill=tk.X, expand=True)

        self._sart_pack = we.ManagedPack()
        self._sart_iterations = we.IntField(self._method_options, 'Iterations', 1)
        self._sart_iterations.configure(**self.theme)
        self._sart_iterations.configure_label(**self.theme)
        self._sart_pack.add(self._sart_iterations, fill=tk.X, expand=True)

        self._sart_relaxation = we.FloatField(self._method_options, 'Relaxation', 0.15)
        self._sart_relaxation.configure(**self.theme)
        self._sart_relaxation.configure_label(**self.theme)
        self._sart_pack.add(self._sart_relaxation, fill=tk.X, expand=True)

        # Options -- Reconstruction method observer: updates managed packs
        self._method.add_observer(self.__method_observer)

        # endregion
        self._input_config_opts = tk.LabelFrame(self.work_area)
        self._input_config_opts.place(relx=0.01, rely=0.8, relheight=0.2, relwidth=0.6)
        self._input_config_opts.configure(relief='groove')
        self._input_config_opts.configure(text='Input configuration')
        self._input_config_opts.configure(**self.theme)
        # endregion

        self._process_start = tk.Button(master=self.work_area, text='Reconstruct', command=self.reconstruct)
        self._process_start.configure(**self.theme)
        self._process_start.place(relx=0.01, rely=0.71, relheight=0.05, relwidth=0.25)

        # Input configuration options -- Source image browser
        self._intput_dir = we.DirBrowser(t_master=self._input_config_opts, label_text='Input directory', t_max_len=32)
        self._intput_dir.configure(**self.theme)
        self._intput_dir.configure_label(**self.theme)
        self._intput_dir.pack(fill=tk.X, expand=True)
        self._intput_dir.place(relx=0.01, rely=0.01, relwidth=0.98)

        self._process_start = tk.Button(master=self._input_config_opts, text='Load images', command=self.load_images)
        self._process_start.configure(**self.theme)
        self._process_start.place(relx=0.01, rely=0.3)

    # todo add events for save/load
    def save_input(self):
        t_dir = filedialog.askdirectory(initialdir='/', title='Select directory to save input')
        opts = {
            'filepath': t_dir
        }
        s_save_images.send(**opts)
        # raise NotImplementedError()

    def save_sinogram(self, name):
        raise NotImplementedError()

    def save_reconstruction(self, name):
        raise NotImplementedError()

    @property
    def load_options(self):
        return {
            'input_dir': self.input_dir,
            'resolution': self.resolution,
            'padding': self.padding
        }

    @property
    def reconstruction_options(self):
        return {
            'method': self.method,
            'nthreads': self.nthreads,
            'start_angle': self.start_angle,
            'end_angle': self.end_angle,
            'fbp_filter': self.fbp_filter,
            'fbp_interpolation': self.fbp_interpolation,
            'sart_iterations': self.sart_iterations,
            'sart_relaxation': self.sart_relaxation
        }

    def load_images(self):
        s_load_images.send(**self.load_options)

    def reconstruct(self):
        s_reconstruct.send(**self.reconstruction_options)

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
        return 'linear'

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
        self.root.mainloop()

    def __method_observer(self, *args):
        if self._method.get() == 0:
            self._method_options.config(text='FBP')
            self._sart_pack.pack_forget()
            self._fbp_pack.pack()
        else:
            self._method_options.config(text='SART')
            self._fbp_pack.pack_forget()
            self._sart_pack.pack()
