import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from src import callbacks

_g_button_options = {'padx': 5, 'pady': 5}


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


class Field:
    def __init__(self, t_master, t_text='', t_validation=None, t_default=None, t_enabled=True):
        self.frame = tk.Frame(t_master)

        self.label = tk.Label(self.frame, text=t_text)
        self.label.pack(side=tk.LEFT)

        if t_enabled:
            self.frame.pack(fill=tk.X, expand=True)

        if t_validation is not None:
            self.entry = tk.Entry(self.frame, validate='key', validatecommand=(t_validation, '%P'))
        else:
            self.entry = tk.Entry(self.frame)
        self.entry.pack(side=tk.RIGHT)

        if t_default is not None:
            self.entry.insert(0, t_default)

    def get(self):
        return self.entry.get()

    def pack(self, **kwargs):
        self.frame.pack(kwargs)

    def pack_forget(self):
        self.frame.pack_forget()


class FloatField(Field):
    def __init__(self, t_master, t_text='', t_default=None, t_enabled=True):
        validation = t_master.register(callbacks.is_float_callback)
        super().__init__(t_master, t_text, validation, t_default, t_enabled=t_enabled)


class IntField(Field):
    def __init__(self, t_master, t_text='', t_default=None, t_enabled=True):
        validation = t_master.register(callbacks.is_int_callback)
        super().__init__(t_master, t_text, validation, t_default, t_enabled=t_enabled)


class RadioMenu:
    def __init__(self, t_master, default=0, observer=None):
        self.frame = tk.Frame(t_master)
        self.frame.pack(fill=tk.X, expand=True)
        self.is_vertical = True
        self.var = tk.IntVar()
        self.var.set(0)
        if observer is not None:
            self.var.trace('r', observer)

    def add_option(self, t_text, t_val, t_row, t_col):
        r = tk.Radiobutton(self.frame, text=t_text, value=t_val, variable=self.var)
        r.grid(row=t_row, column=t_col)

    def add_observer(self, observer):
        self.var.trace('r', observer)

    def get(self):
        return self.var.get()


class Dropdown:
    def __init__(self, t_master, t_text='', t_values=None, t_enabled=True, t_default=0):
        if t_values is None:
            t_values = []

        self.frame = tk.Frame(t_master)

        if t_enabled:
            self.frame.pack(fill=tk.X, expand=True)

        self.label = tk.Label(self.frame, text=t_text)
        self.label.pack(side=tk.LEFT)

        self.combobox = ttk.Combobox(master=self.frame, values=t_values)
        self.combobox.current(t_default)
        self.combobox.pack(side=tk.RIGHT)

    def get(self):
        return self.combobox.get()

    def pack(self, **kwargs):
        self.frame.pack(kwargs)

    def pack_forget(self):
        self.frame.pack_forget()


class DirBrowser:
    def __init__(self, t_master, t_max_len):
        self.frame = tk.Frame(t_master)
        self.frame.pack(fill=tk.X, expand=True)

        self.btn_browse = tk.Button(self.frame, text='Browse', command=self.browse_directory)
        self.btn_browse.pack(side=tk.RIGHT)
        self.dir = ''
        self.label = tk.Label(self.frame, text='')
        self.label.pack(side=tk.LEFT)
        self.max_len = t_max_len

    def browse_directory(self):
        self.dir = filedialog.askdirectory(initialdir='/', title='Select input directory')
        self.label.configure(text="..{}".format(self.dir[self.max_len:]) if len(self.dir) > self.max_len else self.dir)

    def get(self):
        return self.dir


class SaveAs(tk.Frame):
    def __init__(self, master, text='', file_options=None, save_fcn=None):
        super().__init__(master)
        if file_options is None:
            file_options = {}

        self.save_fcn = save_fcn

        btn_options = {'fill': tk.BOTH}
        tk.Button(self, text=text, command=self._saveas).pack(**dict(_g_button_options, **btn_options))

        self.file_options = file_options
        file_options['parent'] = master

    def _saveas(self):
        fname = filedialog.asksaveasfilename(**self.file_options)
        if fname:
            if self.save_fcn is None:
                return open(fname, 'w')
            else:
                self.save_fcn(fname)
