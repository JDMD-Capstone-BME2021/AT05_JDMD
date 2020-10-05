import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from gui import callbacks


class ManagedPack:
    def __init__(self):
        self.elements = []

    def add(self, t_element, **pack_options):
        self.elements.append((t_element, pack_options))

    def pack(self):
        for idx, val in enumerate(self.elements):
            val[0].pack(**val[1])

    def pack_forget(self):
        for idx, val in enumerate(self.elements):
            val[0].pack_forget()


class Field(tk.Frame):
    def __init__(self, t_master, t_text='', t_validation=None, t_default=None):
        super().__init__(t_master)

        self.label = tk.Label(self, text=t_text)
        self.label.pack(side=tk.LEFT)

        if t_validation is not None:
            self.entry = tk.Entry(self, validate='key', validatecommand=(t_validation, '%P'))
        else:
            self.entry = tk.Entry(self)
        self.entry.pack(side=tk.RIGHT)

        if t_default is not None:
            self.entry.insert(0, t_default)

    def get(self):
        return self.entry.get()

    def configure_label(self, **kw):
        self.label.configure(**kw)


class FloatField(Field):
    def __init__(self, t_master, t_text='', t_default=None):
        validation = t_master.register(callbacks.is_float_callback)
        super().__init__(t_master, t_text, validation, t_default)

    def get(self):
        return float(super(FloatField, self).get())


class IntField(Field):
    def __init__(self, t_master, t_text='', t_default=None):
        validation = t_master.register(callbacks.is_int_callback)
        super().__init__(t_master, t_text, validation, t_default)

    def get(self):
        return int(super(IntField, self).get())


class RadioMenu(tk.Frame):
    def __init__(self, t_master, default=0, observer=None, **kw):
        super().__init__(t_master, **kw)
        self.pack(fill=tk.X, expand=True)
        self.is_vertical = True
        self.var = tk.IntVar()
        self.var.set(default)
        self.rb = []
        if observer is not None:
            self.var.trace('r', observer)

    def add_option(self, t_text, t_val, t_row, t_col):
        self.rb.append(tk.Radiobutton(self, text=t_text, value=t_val, variable=self.var))
        self.rb[-1].grid(row=t_row, column=t_col)

    def add_observer(self, observer):
        self.var.trace('r', observer)

    def get(self):
        return self.var.get()

    def set_theme(self, **kw):
        for i, e in enumerate(self.rb):
            e.configure(**kw)


class Dropdown(tk.Frame):
    def __init__(self, t_master, t_text='', t_values=None, t_default=0):
        super().__init__(t_master)
        if t_values is None:
            t_values = []

        self.label = tk.Label(self, text=t_text)
        self.label.pack(side=tk.LEFT)

        self.combobox = ttk.Combobox(master=self, values=t_values)
        self.combobox.current(t_default)
        self.combobox.pack(side=tk.RIGHT)

    def configure_label(self, **kwargs):
        self.label.configure(**kwargs)

    def configure_combobox(self, **kwargs):
        self.combobox.configure(**kwargs)

    def get(self):
        return self.combobox.get()


class DirBrowser(tk.Frame):
    def __init__(self, t_master, t_max_len, label_text='', **kw):
        super().__init__(t_master, **kw)

        self.btn_browse = tk.Button(self, text='Browse', command=self.browse_directory)
        self.btn_browse.pack(side=tk.RIGHT)
        self.dir = ''
        self.label = tk.Label(self, text=label_text)
        self.label.pack(side=tk.LEFT)
        self.max_len = t_max_len

    def browse_directory(self):
        self.dir = filedialog.askdirectory(initialdir='/', title='Select input directory')
        self.label.configure(text="..{}".format(self.dir[self.max_len:]) if len(self.dir) > self.max_len else self.dir)

    def get(self):
        return self.dir

    def configure_label(self, **kw):
        self.label.configure(**kw)


class SaveAs(tk.Frame):
    def __init__(self, master, text='', file_options=None, save_fcn=None, **kw):
        super().__init__(master, **kw)
        if file_options is None:
            file_options = {}

        self.save_fcn = save_fcn

        self.btn = tk.Button(self, text=text, command=self._saveas)
        self.btn.pack()

        self.file_options = file_options
        file_options['parent'] = master

    def configure_btn(self, **kw):
        self.btn.configure(**kw)

    def _saveas(self):
        fname = filedialog.asksaveasfilename(**self.file_options)
        if fname:
            if self.save_fcn is None:
                return open(fname, 'w')
            else:
                self.save_fcn(fname)


class ImgView(tk.Canvas):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self._image = None
        self._render = None

    def set_image(self, image: Image, sz=(256, 256)):
        self._image = image.resize(sz)
        self._render = ImageTk.PhotoImage(self._image)
        self.delete('all')
        self.create_image(sz[0] // 2, sz[1] // 2, image=self._render)
