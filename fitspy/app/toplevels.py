"""
Module dedicated to external widgets (Tkinter.Toplevel) creation
"""
from tkinter import Toplevel, Label, Entry, Button, Checkbutton, Text, Scrollbar
from tkinter import IntVar, StringVar, BooleanVar, W, E, END, RIGHT
from tkinter.ttk import Combobox
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex
from lmfit import fit_report

from fitspy.spectra import MODELS, KEYS
from fitspy.app.utils import add, add_entry
from fitspy.app.callbacks import FIT_METHODS

LABELS = ['x0', 'ampli', 'fwhm', 'fwhm (left)', 'fwhm (right)', 'alpha']
CMAP = plt.get_cmap("tab10")
NCPUS = ['auto', 1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32]


class TabView:
    """ Class for spectra models fit results and parameters displaying """

    def __init__(self, root):

        self.frame = Toplevel(root)
        self.frame_stats = Toplevel(root)

        # hide the frames
        self.frame.withdraw()
        self.frame_stats.withdraw()
        self.hidden = True

        # make the frame remain on top until destroyed and disable closing
        self.frame.attributes('-topmost', 'true')
        self.frame.protocol("WM_DELETE_WINDOW", lambda *args: None)
        self.frame_stats.attributes('-topmost', 'true')
        self.frame_stats.protocol("WM_DELETE_WINDOW", lambda *args: None)

        self.spectrum = None
        self.params = None
        self.models = None
        self.models_delete = None
        self.plot = None

        self.show_bounds = BooleanVar(value=False)
        self.show_expr = BooleanVar(value=False)

        vsbar = Scrollbar(self.frame_stats, orient='vertical')
        vsbar.pack(side=RIGHT, fill='y')
        self.text = Text(self.frame_stats, yscrollcommand=vsbar.set)
        vsbar.config(command=self.text.yview)

    def add_entry(self, arg, row, col, i, key, param):
        """ Add Tk.Entry at (row, col) linked to params[i][key][arg] """
        if arg == 'expr':
            width, cspan, val = 36, 3, f'{param[arg]}'
        else:
            width, cspan, val = 10, 1, f'{param[arg]:.4g}'

        var = StringVar()
        entry = Entry(self.frame, textvariable=var, width=width,
                      validate="focusout",
                      validatecommand=lambda i=i, key=key, arg=arg:
                      self.param_has_changed(i, key, arg))
        entry.insert(0, val)
        add(entry, row, col, cspan=cspan)
        entry.bind('<Return>', lambda _, key=key, arg=arg,
                                      i=i: self.param_has_changed(i, key, arg))
        self.params[i][key][arg] = var

    def add_check_button(self, arg, row, col, i, key, param):
        """ Add Tk.Checkbutton at (row, col) linked to params[i][key][arg] """
        var = BooleanVar(value=not param[arg])
        cbut = Checkbutton(self.frame, variable=var,
                           command=lambda i=i, key=key, arg=arg:
                           self.param_has_changed(i, key, arg))
        add(cbut, row, col)
        self.params[i][key][arg] = var

    def add_entry_models_labels(self, row, col, i):
        """ Add Tk.Entry at (row, col) linked to models_labels[i] """
        model_label = StringVar(value=self.spectrum.models_labels[i])
        entry = Entry(self.frame, textvariable=model_label, width=8)
        add(entry, row, col)
        entry.bind('<Return>', lambda event, i=i: self.label_has_changed(i))
        self.models_labels.append(model_label)

    def add_combobox_models(self, row, col, i, model):
        """ Add Tk.Combobox at (row, col) linked to models[i] """
        model_name = StringVar(value=self.spectrum.get_model_name(model))
        cbox = Combobox(self.frame, values=list(MODELS.keys()),
                        textvariable=model_name, width=15)
        add(cbox, row, col)
        cbox.bind('<<ComboboxSelected>>',
                  lambda event, i=i: self.model_has_changed(i))
        self.models.append(model_name)

    def label_has_changed(self, i):
        """ Update the label related to the ith-model """
        self.spectrum.models_labels[i] = self.models_labels[i].get()
        self.plot()  # pylint:disable=not-callable
        self.update()

    def param_has_changed(self, i, key, arg):
        """ Update the 'key'-param 'arg'-value related to the ith-model """
        value = self.params[i][key][arg].get()
        param = self.spectrum.models[i].param_hints[key]

        if arg == 'vary':
            value = not bool(value)
        elif arg == 'expr':
            pass
        else:  # 'value', 'min', 'max'
            value = float(self.params[i][key][arg].get())
            if arg == 'value':
                value = max(min(param['max'], value), param['min'])
                self.params[i][key][arg].set(f'{value:.4g}')  # bound the value
        param[arg] = value
        self.spectrum.result_fit = None
        self.plot()  # pylint:disable=not-callable

    def model_has_changed(self, i):
        """ Update the model function related to the ith-model """
        spectrum = self.spectrum
        old_model_name = self.spectrum.get_model_name(spectrum.models[i])
        new_model_name = self.models[i].get()
        if new_model_name != old_model_name:
            ampli = spectrum.models[i].param_hints['ampli']['value']
            x0 = spectrum.models[i].param_hints['x0']['value']
            spectrum.models[i] = spectrum.create_model(new_model_name, i + 1,
                                                       ampli=ampli, x0=x0)
            self.spectrum.result_fit = None
            self.plot()  # pylint:disable=not-callable
            self.update()

    def set_header(self):
        """ Set the TabView header """
        frame = self.frame

        add(Checkbutton(frame, text='show bounds', variable=self.show_bounds,
                        command=self.update), 0, 3, W)
        add(Checkbutton(frame, text='show expressions', variable=self.show_expr,
                        command=self.update), 1, 3, W)

        add(Button(frame, text='Del.', command=self.delete_models), 2, 0)
        add(Label(frame, text='prefix', width=5), 2, 1)
        add(Label(frame, text='labels', width=5), 2, 2)
        add(Label(frame, text='models', width=10), 2, 3)

        for j, label in enumerate(LABELS):
            add(Label(frame, text=label, width=10), 2, 4 * j + 5)

    def delete_models(self):
        """ Delete selected models """
        nb_models = len(self.models_delete)
        for i, val in enumerate(reversed(self.models_delete)):
            if val.get():
                self.spectrum.del_model(nb_models - i - 1)
                self.spectrum.result_fit = None
        self.plot()  # pylint:disable=not-callable
        self.update()

    def update(self):
        """ Update the Tabview """
        self.delete()

        if len(self.spectrum.models) == 0:
            return

        self.models = []
        self.models_delete = []
        self.models_labels = []
        self.params = {}
        row = 3
        for i, model in enumerate(self.spectrum.models):

            var = BooleanVar(value=False)
            add(Checkbutton(self.frame, variable=var), row, 0)
            self.models_delete.append(var)

            add(Label(self.frame, text=model.prefix, font='Helvetica 10 bold',
                      fg=rgb2hex(CMAP(i % CMAP.N)), width=4), row, 1)

            self.add_entry_models_labels(row, 2, i)

            self.add_combobox_models(row, 3, i, model)

            params = model.param_hints
            self.params[i] = {}
            for k, key in enumerate(KEYS):
                if key not in params.keys():
                    continue
                param = params[key]
                self.params[i][key] = {}
                col = 4 * k + 4
                self.add_entry('value', row, col + 1, i, key, param)
                self.add_check_button('vary', row, col + 3, i, key, param)

                if self.show_bounds.get():
                    self.add_entry('min', row, col, i, key, param)
                    self.add_entry('max', row, col + 2, i, key, param)

                if self.show_expr.get():
                    self.add_entry('expr', row + 1, col, i, key, param)
            row += 2

    def update_stats(self):
        """ Update the statistics """
        self.text.delete(1.0, END)
        if self.spectrum.result_fit is not None:
            self.text.insert(END, fit_report(self.spectrum.result_fit))
            self.text.pack()

    def delete(self):
        """ Delete all the values contained in frames """
        self.text.delete(1.0, END)
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.set_header()

    def show_hide(self):
        """ Show/Hide the TopLevel frame """
        if not self.hidden:
            self.frame.withdraw()
            self.frame_stats.withdraw()
            self.hidden = True
        else:
            self.frame.deiconify()
            self.frame_stats.deiconify()
            self.hidden = False


class Settings:
    """ Master class for parameters setting """

    def __init__(self, root):
        self.frame = Toplevel(root,
                              highlightbackground="black",
                              highlightthickness=1)

        # hide the frame
        self.frame.withdraw()
        self.hidden = True

        # make the frame remain on top until destroyed and disable closing
        self.frame.attributes('-topmost', 'true')
        self.frame.overrideredirect(True)
        self.frame.bind('<FocusOut>', self.on_press)

    def frame_creation(self, bind_fun, excluded_keys=None):
        """ Create frame with 'params' linked to 'bind_fun' """
        params = self.params.copy()
        if excluded_keys is not None:
            [params.pop(key) for key in excluded_keys]

        for row, (key, val) in enumerate(params.items()):
            text = key.replace('_', ' ')
            if isinstance(val, IntVar):
                add_entry(self.frame, row, text, val, bind_fun=bind_fun)
            elif isinstance(val, StringVar):
                cbox = Combobox(self.frame, values=['On', 'Off'],
                                textvariable=val, width=5)
                add(Label(self.frame, text=text), row, 0, E)
                add(cbox, row, 1, W)
                if bind_fun is not None:
                    cbox.bind("<<ComboboxSelected>>", lambda event: bind_fun())
            else:
                raise NotImplementedError

    def update(self, x, y, bind_fun=None):
        """ Display the Toplevel 'frame' on (x, y) position with interactive
            'params' settings """
        self.show_hide()
        self.frame.geometry(f"+{x}+{y}")
        self.frame_creation(bind_fun)

    def on_press(self, _):
        """ Hide the Toplevel 'frame' if the mouse click is outside """
        if not self.frame.tk.call('focus'):
            self.hidden = False
            self.show_hide()

    def show_hide(self):
        """ Show/Hide the TopLevel 'frame' """
        if not self.hidden:
            self.frame.withdraw()
            self.hidden = True
        else:
            self.frame.deiconify()
            self.hidden = False


class AttractorsSettings(Settings):
    """ Class for attractors parameters setting """

    def __init__(self, root):
        super().__init__(root)
        self.params = {'distance': IntVar(value=20),
                       'prominence': IntVar(value=None),
                       'width': IntVar(value=None),
                       'height': IntVar(value=None),
                       'threshold': IntVar(value=None)}


class FitSettings(Settings):
    """ Class for fitting parameters setting """

    def __init__(self, root):
        super().__init__(root)
        self.params = {'fit_negative_values': StringVar(value='Off'),
                       'maximum_iterations': IntVar(value=200),
                       'fit_method': StringVar(value='Leastsq'),
                       'ncpus': StringVar(value='auto')}

    def frame_creation(self, bind_fun, excluded_keys=None):
        excluded_keys = ['fit_method', 'ncpus']
        super().frame_creation(bind_fun, excluded_keys=excluded_keys)

        add(Label(self.frame, text='fit method'), 2, 0, E)
        add(Combobox(self.frame, values=list(FIT_METHODS.keys()),
                     textvariable=self.params['fit_method'], width=12), 2, 1, W)

        add(Label(self.frame, text='Number of CPUs'), 3, 0, E)
        add(Combobox(self.frame, values=NCPUS,
                     textvariable=self.params['ncpus'], width=6), 3, 1, W)


class FigureSettings(Settings):
    """ Class for figure parameters setting """

    def __init__(self, root):
        super().__init__(root)
        self.params = {'plot_fit': StringVar(value='On'),
                       'plot_negative_values': StringVar(value='On'),
                       'plot_residual': StringVar(value='Off'),
                       'coef_residual': IntVar(value=1),
                       'show_peaks_labels': StringVar(value='On'),
                       'title': StringVar(value='DEFAULT'),
                       'x_label': StringVar(value=''),
                       'y_label': StringVar(value='')}

    def frame_creation(self, bind_fun, excluded_keys=None):
        excluded_keys = ['title', 'x_label', 'y_label']
        super().frame_creation(bind_fun, excluded_keys=excluded_keys)

        add_entry(self.frame, 6, 'title', self.params['title'], width=10,
                  bind_fun=bind_fun)

        add_entry(self.frame, 7, 'x-label', self.params['x_label'], width=10,
                  bind_fun=bind_fun)

        add_entry(self.frame, 8, 'y-label', self.params['y_label'], width=10,
                  bind_fun=bind_fun)


if __name__ == '__main__':
    import tkinter as tk
    from fitspy.spectra import Spectrum

    my_spectrum = Spectrum()
    my_spectrum.models = [Spectrum.create_model('Lorentzian', i, ampli=10 * i,
                                                x0=100 * i) for i in range(5)]

    my_root = tk.Tk()
    tabview = TabView(my_root)
    tabview.hidden = True
    tabview.spectrum = my_spectrum
    tabview.plot = print
    tabview.set_header()
    tabview.update()
    tabview.show_hide()
    my_root.mainloop()
