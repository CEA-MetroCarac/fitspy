"""
utilities functions related to Tkinter
"""
import os
import glob
from itertools import groupby, count
from tkinter import (LabelFrame, Frame, Label, Entry, Canvas, Scrollbar, Button,
                     Listbox, Variable, StringVar)
from tkinter import W, E, HORIZONTAL, EXTENDED, BOTTOM, X, Y, LEFT, RIGHT, END
from tkinter import filedialog as fd

from fitspy.utils import hsorted


def add(obj, row, col, sticky='', padx=5, pady=3, rspan=1, cspan=1, **kwargs):
    """ Add tkinter object at the (row, col)-position of a grid """
    obj.grid(row=row, column=col, sticky=sticky, padx=padx, pady=pady,
             rowspan=rspan, columnspan=cspan, **kwargs)


def add_entry(frame, row, label, val, width=5, bind_fun=None):
    """ Add 2 columns : 'label' and 'val' associated to a binding function
        'bind_fun' at 'row' (int) position in a 'frame' (Tk.Frame) """
    add(Label(frame, text=label), row, 0, E)
    entry = Entry(frame, textvariable=val, width=width)
    add(entry, row, 1, W)
    if bind_fun is not None:
        entry.bind('<Return>', lambda event: bind_fun())


def interactive_entry(root, var, fun, width=2):
    """ Return an interactive Tkinter.Entry binded to 'fun' """

    def validate(value, fun):
        try:
            value.get()
            fun()
        except Exception:
            pass

    var.trace('w', lambda name, idx, mode, var=var, fun=fun: validate(var, fun))
    entry = Entry(root, textvariable=var, width=width)
    return entry


def dict_has_tk_variable(dictionary):
    """ Return 'True' if 'dictionary' has Tkinter.Variable as value """
    for x in list(dictionary.values()):
        if isinstance(x, Variable):
            return True
    return False


def convert_dict_from_tk_variables(parent_dict, excluded_keys=None):
    """ Convert a dictionary from Tkinter.Variables to standard types
        (thanks to a recursive processing)   """
    excluded_keys = excluded_keys or []

    new_dict = {}
    for key, val in parent_dict.items():
        if key in excluded_keys:
            new_dict[key] = val
        elif isinstance(val, dict):
            new_dict[key] = convert_dict_from_tk_variables(val)
        elif isinstance(val, list):
            new_dict[key] = [x.get() for x in val]
        else:
            new_dict[key] = val.get()
    return new_dict


class ToggleFrame(LabelFrame):
    """ Class dedicated to Enable/Disable LabelFrame and its related children"""

    def __init__(self, master, exceptions=None, **kwargs):
        super().__init__(master=master, **kwargs)
        self.exceptions = exceptions or []
        self.is_enable = True

    def apply_state(self, state, parent=None):
        """ Apply state 'disable' or 'normal' to Frame's children widgets """
        parent = parent or self
        for child in parent.winfo_children():
            if not isinstance(child, Frame):
                config = child.configure()
                if 'text' in config and config['text'][-1] in self.exceptions:
                    continue
                try:
                    child.configure(state=state)
                except:  # pylint:disable=bare-except
                    pass
            else:
                self.apply_state(state, child)

    def disable(self):
        """ Disable Frame's children widgets """
        self.is_enable = False
        self.config(fg="gray")
        self.apply_state(state='disable')

    def enable(self):
        """ Enable Frame's children widgets """
        self.is_enable = True
        self.config(fg="black")
        self.apply_state(state='normal')


class ScrollbarFrame:
    """
    Class to add a vertical and/or horziontal Scrollbar to a frame.
    (Strongly inspired from https://stackoverflow.com/questions/43731784)

    Attributes
    ----------
    frame_canvas: Tkinter.Frame
        Frame gathers the 'Canvas' and the 'Scrollbar' objects
    canvas: Tkinter.Canvas
        Canvas related to the first (large) row-column
    vsbar: Tkinter.Scrollbar
        Vertical scrollbar related to the 2nd (small) column, if 'orientation'
        is 'vertical' or 'both'
    hsbar: Tkinter.Scrollbar
        Horizontal scrollbar related to the 2nd (small) row if 'orientation'
        is 'horizontal' or 'both'
    frame: Tkinter.Frame
        Frame included in the canvas, where other frames can be stacked

    Parameters
    ----------
    root: Tkinter parent window
    orientation: str, optional
        Orientation associated to the scrollbar(s), among ['vertical',
        'horizontal', 'both']
    """

    def __init__(self, root, orientation='both'):

        orients = ['vertical', 'horizontal', 'both']
        assert orientation in orients, f"'orientation should be in {orients}"

        self.frame_canvas = Frame(root)
        self.frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
        self.frame_canvas.grid_rowconfigure(0, weight=1)
        self.frame_canvas.grid_columnconfigure(0, weight=1)
        self.frame_canvas.grid_propagate(False)

        self.canvas = Canvas(self.frame_canvas)
        self.canvas.grid(row=0, column=0, sticky="news")

        self.frame = Frame(self.canvas)

        self.vsbar = None
        self.hsbar = None

        if orientation in ['vertical', 'both']:
            self.vsbar = Scrollbar(self.frame_canvas, orient="vertical",
                                   command=self.canvas.yview)
            self.vsbar.grid(row=0, column=1, sticky='ns')
            self.canvas.configure(yscrollcommand=self.vsbar.set)

        if orientation in ['horizontal', 'both']:
            self.hsbar = Scrollbar(self.frame_canvas, orient="horizontal",
                                   command=self.canvas.xview)
            self.hsbar.grid(row=1, column=0, sticky='we')
            self.canvas.configure(xscrollcommand=self.hsbar.set)

        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

    def update_and_resize(self, width=None, height=None):
        """
        Set the scrolling region with the 'correct' size

        Parameters
        ----------
        width: int, optional
            Width of the canvas frame.
            If None, consider the 'frame' width.
        height: int, optional
            height of the canvas frame.
            If None, consider the minimum between the frame height and 90% of
            the screen height
        """
        self.frame.update_idletasks()

        if width is None:
            width = self.frame.winfo_width() + self.vsbar.winfo_width()
        if height is None:
            height = min(self.frame.winfo_height() + 4,
                         int(0.9 * self.frame.winfo_screenheight()))

        # Set the canvas scrolling region to the 'correct' size
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.frame_canvas.config(width=width, height=height)


class FilesSelector:
    """
    Class dedicated to the files selection

    Attributes
    ----------
    ninputs: int
        Number of inputs to consider
    lbox: list of Listbox object
        List of 'ninputs'-Listbox associated to the selected files
    filenames: list of str
        List of 'ninputs'-list of filenames to work with
    files_extension: iterable of str
        Extension used for the files selection
    self.dirname_res: str
        Directory pathname where to find results associated to the files

    Parameters
    ----------
    root: Tk.widget
        The main window associated to the FileSelector
    ninputs: int, optional
        Number of inputs to consider
    files_extensions: str, optional
        Extension used for files selection.
    dirname_results: str, optional
        Directory pathname where to find results associated to the files
        'DEFAULT' value refers to './results' directory associated to the 'file'
        location
    lbox_size: list of 2 ints, optional
        Size (width, height) of the Listbox 'lbox'. Default value is [30, 15]
    options: dict, optional
        Dictionary of options
    tab_options: Frame object
        Tab dedicated to options parameters settings
    """

    def __init__(self, root,
                 ninputs=1,
                 files_extensions='*.txt',
                 dirname_results='DEFAULT',
                 lbox_size=None,
                 options=None, tab_options=None):

        lbox_size = lbox_size or [30, 15]
        if options is None:
            options = {}

        self.ninputs = ninputs
        self.lbox = []
        self.options = options

        self.filenames = [[] for _ in range(ninputs)]

        self.options['files_extension'] = files_extensions
        self.options['dirname_results'] = dirname_results

        # create buttons/listbox associated to each input
        for i in range(self.ninputs):
            inc = 3 * i

            Button(root, text="Select Files",
                   command=lambda ind=i: self.select_files(ind)). \
                grid(column=0, row=0 + inc, padx=0, pady=5)
            Button(root, text="Select Dir.",
                   command=lambda ind=i: self.select_dir(ind)). \
                grid(column=1, row=0 + inc, padx=0, pady=5)
            Button(root, text="Remove",
                   command=lambda ind=i: self.remove(ind)). \
                grid(column=2, row=0 + inc, padx=0, pady=5)
            Button(root, text="Remove all",
                   command=lambda ind=i: self.remove_all(ind)). \
                grid(column=3, row=0 + inc, padx=0, pady=5)

            if i == 0:
                Button(root, text="▲", command=lambda: self.move('up')). \
                    grid(column=1, row=1 + inc, pady=0, sticky=E)
                Button(root, text="▼", command=lambda: self.move('down')). \
                    grid(column=2, row=1 + inc, pady=0, sticky=W)

            lbox_frame = Frame(root)
            lbox_frame.grid(column=0, row=2 + inc, padx=5, pady=0, columnspan=4)
            sbar_v = Scrollbar(lbox_frame)
            sbar_h = Scrollbar(lbox_frame, orient=HORIZONTAL)
            self.lbox.append(Listbox(lbox_frame,
                                     width=lbox_size[0],
                                     height=lbox_size[1],
                                     selectmode=EXTENDED,
                                     exportselection=False,
                                     yscrollcommand=sbar_v.set,
                                     xscrollcommand=sbar_h.set))

            sbar_v.config(command=self.lbox[i].yview)
            sbar_h.config(command=self.lbox[i].xview)

            sbar_h.pack(side=BOTTOM, fill=X)
            self.lbox[i].pack(side=LEFT, fill=Y)
            sbar_v.pack(side=RIGHT, fill=Y)

        # Options Tab
        if tab_options is not None:
            frame = LabelFrame(tab_options, text='Files options')
            frame.grid(column=0, row=0, padx=5, pady=5)

            Label(frame, text='files extensions :'). \
                grid(column=0, row=0, padx=5, pady=5, sticky=E)
            self.files_extension = StringVar(
                value=self.options['files_extension'])
            Entry(frame, textvariable=self.files_extension, width=20). \
                grid(column=1, row=0, padx=5, pady=5, sticky=W)

            Label(frame, text='dirname results :'). \
                grid(column=0, row=1, padx=5, pady=5, sticky=E)
            self.dirname_res = StringVar(value=self.options['dirname_results'])
            Entry(frame, textvariable=self.dirname_res, width=20). \
                grid(column=1, row=1, padx=5, pady=5, sticky=W)

    def set_options(self):
        """ Set files options """
        self.options['files_extension'] = self.files_extension.get()
        self.options['dirname_results'] = self.dirname_res.get()

    def synchronize(self):
        """ Cursor selection synchronization between Listbox """
        indices = self.lbox[0].curselection()
        for i in range(self.ninputs):
            self.lbox[i].selection_clear(0, END)
            for ind in indices:
                self.lbox[i].selection_set(ind)

    def move(self, key):
        """ Move cursor selection according to key value (up or down) """
        increment = {'up': -1, 'down': 1, 'none': 0}
        indices = self.lbox[0].curselection()
        if not indices:
            return
        ind = min(indices)  # working with several indices has no sense
        if len(indices) > 1:
            key = 'none'
        elif (key == 'up' and ind == 0) or \
                (key == 'down' and ind == len(self.filenames[0]) - 1):
            return
        for i in range(self.ninputs):
            self.lbox[i].selection_clear(0, END)
            self.lbox[i].selection_set(ind + increment[key])

        self.synchronize()
        self.lbox[0].event_generate('<<ListboxSelect>>')

    def add_items(self, i=0, filenames=None, ind_start=None):
        """ Add items from a 'filenames' list """

        ind_start = ind_start or len(self.filenames[i])

        for fname in hsorted(filenames):
            self.lbox[i].insert(END, os.path.basename(fname))
            self.filenames[i].append(fname)

        # select the first new item
        for k in range(self.ninputs):
            self.lbox[i].selection_clear(0, END)
            self.lbox[k].select_set(ind_start)

        self.synchronize()

    def select_files(self, i=0, filenames=None):
        """ Add items from selected files """

        if filenames is None:
            files_ext = self.options['files_extension']
            filetypes = (('', files_ext), ('All files', '*.*'))
            filenames = fd.askopenfilenames(title='Select file(s)',
                                            filetypes=filetypes)
        self.add_items(i=i, filenames=filenames)

        self.lbox[0].event_generate('<<ListboxAdd>>')

    def select_dir(self, i=0, dirname=None):
        """ Add items from a directory """
        if dirname is None:
            dirname = fd.askdirectory(title='Select directory')

        ind_start = len(self.filenames[i])
        for files_ext in self.options['files_extension'].split():
            filenames = glob.glob(os.path.join(dirname, files_ext))
            self.add_items(i, filenames, ind_start=ind_start)

        self.lbox[0].event_generate('<<ListboxAdd>>')

    def remove(self, i=0):
        """ Remove selected items """
        selected_items = self.lbox[i].curselection()

        # deleting one by one item is too long when working with a big selection
        groups = groupby(selected_items, key=lambda n, c=count(): n - next(c))
        groups = [list(g) for _, g in groups]
        for group in groups:
            for k in range(self.ninputs):
                self.lbox[k].delete(group[0], group[-1])

        for selected_item in reversed(selected_items):
            for k in range(self.ninputs):
                self.filenames[k].pop(selected_item)

        # reselect the first item
        for k in range(self.ninputs):
            self.lbox[k].select_set(0)

        self.synchronize()
        self.lbox[0].event_generate('<<ListboxRemove>>')

    def remove_all(self, i=0):
        """ Remove all items """
        self.lbox[i].delete(0, END)
        self.filenames[i] = []
        self.synchronize()
        self.lbox[0].event_generate('<<ListboxRemoveAll>>')
