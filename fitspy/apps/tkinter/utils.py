"""
utilities functions related to Tkinter
"""
import os
import glob
from itertools import groupby, count
from tkinter import (LabelFrame, Frame, Label, Entry, Scrollbar, Button,
                     Listbox, TclError, IntVar)
from tkinter import W, E, HORIZONTAL, EXTENDED, BOTTOM, X, Y, LEFT, RIGHT, END
from tkinter import filedialog as fd
from tkinter.messagebox import showerror
from tkinter.ttk import Progressbar

from fitspy.core.utils import hsorted


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
            try:
                new_dict[key] = val.get()
            except TclError as error:
                msg = str(error) + f" for {key}"
                print("Error in parameter interpretation:", msg)
                showerror(message=msg)
                return
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


class FilesSelector:
    """
    Class dedicated to the files selection

    Attributes
    ----------
    lbox: list of Listbox object
        Listbox associated to the selected files
    filenames: list of str
        List of of filenames to work with

    Parameters
    ----------
    root: Tk.widget
        The main window associated to the FileSelector
    lbox_size: list of 2 ints, optional
        Size (width, height) of the Listbox 'lbox'. Default value is [30, 15]
    """

    def __init__(self, root, lbox_size=None):

        lbox_size = lbox_size or [30, 15]

        self.filenames = []

        # create buttons and listbox

        Button(root, text="Select Files",
               command=self.select_files). \
            grid(column=0, row=0, padx=0, pady=5)
        Button(root, text="Select Dir.",
               command=self.select_dir). \
            grid(column=1, row=0, padx=0, pady=5)
        Button(root, text="Remove",
               command=self.remove). \
            grid(column=2, row=0, padx=0, pady=5)
        Button(root, text="Remove all",
               command=self.remove_all). \
            grid(column=3, row=0, padx=0, pady=5)

        Button(root, text="▲", command=lambda: self.move('up')). \
            grid(column=1, row=1, pady=0, sticky=E)
        Button(root, text="▼", command=lambda: self.move('down')). \
            grid(column=2, row=1, pady=0, sticky=W)

        lbox_frame = Frame(root)
        lbox_frame.grid(column=0, row=2, padx=5, pady=0, columnspan=4)
        sbar_v = Scrollbar(lbox_frame)
        sbar_h = Scrollbar(lbox_frame, orient=HORIZONTAL)
        self.lbox = Listbox(lbox_frame,
                            width=lbox_size[0],
                            height=lbox_size[1],
                            selectmode=EXTENDED,
                            activestyle="underline",
                            exportselection=False,
                            yscrollcommand=sbar_v.set,
                            xscrollcommand=sbar_h.set)

        sbar_v.config(command=self.lbox.yview)
        sbar_h.config(command=self.lbox.xview)

        sbar_h.pack(side=BOTTOM, fill=X)
        self.lbox.pack(side=LEFT, fill=Y)
        sbar_v.pack(side=RIGHT, fill=Y)

    def move(self, key):
        """ Move cursor selection according to key value (up or down) """
        increment = {'up': -1, 'down': 1, 'none': 0}
        indices = self.lbox.curselection()
        if not indices:
            return
        ind = min(indices)  # working with several indices has no sense
        if len(indices) > 1:
            key = 'none'
        elif (key == 'up' and ind == 0) or \
                (key == 'down' and ind == len(self.filenames) - 1):
            return
        ind += increment[key]
        self.select_item(ind)

        self.lbox.event_generate('<<ListboxSelect>>')

    def add_items(self, filenames=None, ind_start=None):
        """ Add items from a 'filenames' list """

        ind_start = ind_start or len(self.filenames)

        for fname in hsorted(filenames):
            self.lbox.insert(END, os.path.basename(fname))
            self.filenames.append(os.path.normpath(fname))

        # select the first new item
        self.select_item(ind_start)

    def select_files(self, filenames=None):
        """ Add items from selected files """

        if filenames is None:
            filenames = fd.askopenfilenames(title='Select file(s)')
        self.add_items(filenames=filenames)

        self.lbox.event_generate('<<ListboxAdd>>')

    def select_dir(self, dirname=None):
        """ Add items from a directory """
        if dirname is None:
            dirname = fd.askdirectory(title='Select directory')

        ind_start = len(self.filenames)
        filenames = glob.glob(os.path.join(dirname, '*.txt'))
        self.add_items(filenames, ind_start=ind_start)

        self.lbox.event_generate('<<ListboxAdd>>')

    def remove(self):
        """ Remove selected items """
        selected_items = self.lbox.curselection()

        # deleting one by one item is too long when working with a big selection
        groups = groupby(selected_items, key=lambda n, c=count(): n - next(c))
        groups = [list(g) for _, g in groups]
        for group in groups:
            self.lbox.delete(group[0], group[-1])

        for selected_item in reversed(selected_items):
            self.filenames.pop(selected_item)

        # reselect the first item
        self.select_item(0)

        self.lbox.event_generate('<<ListboxRemove>>')

    def remove_all(self):
        """ Remove all items """
        self.lbox.delete(0, END)
        self.filenames = []

        self.lbox.event_generate('<<ListboxRemoveAll>>')

    def select_item(self, index, selection_clear=True):
        """ Select item in the listbox """
        if selection_clear:
            self.lbox.selection_clear(0, END)
        self.lbox.selection_set(index)
        self.lbox.activate(index)
        self.lbox.selection_anchor(index)
        self.lbox.see(index)


class ProgressBar:
    """ Class to create a progress bar """

    def __init__(self, frame):
        self.frame = frame
        self.var = IntVar(value=0)
        self.pbar = Progressbar(self.frame, variable=self.var, maximum=100,
                                length=200, mode='determinate')
        self.label_counter = Label(self.frame, text='0/0')
        self.label_ncpus = Label(self.frame, text='ncpus:')

        add(self.label_counter, 0, 0)
        add(self.pbar, 0, 1)
        add(self.label_ncpus, 0, 2)

    def update(self, spectra, ntot, ncpus):
        """ update the progressbar info during the fitspy execution """
        self.label_ncpus['text'] = f"ncpus: {ncpus}"
        self.var.set(0)
        percent = 0
        while percent < 100:
            percent = 100 * (spectra.pbar_index) / ntot
            self.var.set(percent)
            self.label_counter['text'] = f"{spectra.pbar_index}/{ntot}"
            self.frame.update()


if __name__ == '__main__':
    from tkinter import Tk

    my_root = Tk()
    fselector = FilesSelector(my_root)
    fnames = []
    for i in range(20):
        fnames.append(f"File_______________________________{i}")
    fselector.add_items(fnames)
    fselector.select_item(15)
    my_root.mainloop()
