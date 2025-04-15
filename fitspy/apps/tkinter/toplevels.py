"""
Module dedicated to external widgets (Tkinter.Toplevel) creation
"""
import itertools
from tkinter import Toplevel, Label, Entry, Button, Checkbutton, Text, Scrollbar
from tkinter import IntVar, DoubleVar, StringVar, BooleanVar, W, E, END, RIGHT
from tkinter.ttk import Combobox

import numpy as np
from matplotlib.colors import rgb2hex
from lmfit import fit_report
from lmfit.model import ModelResult

from fitspy.apps.tkinter.utils import add, add_entry
from fitspy.apps.tkinter import CMAP, NCPUS
from fitspy import PEAK_MODELS, BKG_MODELS, PEAK_PARAMS, FIT_METHODS, FIT_PARAMS


class ResultView:
    """ Master class used by ParamsView and StatsView """

    def __init__(self, root):

        self.frame = Toplevel(root)

        # hide the frames
        self.frame.withdraw()
        self.hidden = True

        # make the frame remain on top until destroyed and disable closing
        # self.frame.attributes('-topmost', 'true')
        self.frame.protocol("WM_DELETE_WINDOW", lambda *args: None)

        self.spectrum = None

    def show_hide(self):
        """ Show/Hide the TopLevel frame """
        if not self.hidden:
            self.frame.withdraw()
            self.hidden = True
        else:
            self.frame.deiconify()
            self.hidden = False


class ParamsView(ResultView):
    """ Class for models parameters displaying """

    def __init__(self, root):
        super().__init__(root)

        self.params = None
        self.peak_models = None
        self.peak_models_delete = None
        self.peak_labels = None
        self.plot = None

        self.show_bounds = BooleanVar(value=False)
        self.show_expr = BooleanVar(value=False)
        self.bkg_name = StringVar(value='None')

    def add_entry(self, arg, row, col, i, key, param):
        """ Add Tk.Entry at (row, col) linked to params[i][key][arg] """
        if arg == 'expr':
            width, cspan, val = 28, 3, f'{param[arg]}'
        else:
            width, cspan, val = 7, 1, f'{param[arg]:.4g}'

        var = StringVar()
        entry = Entry(self.frame, textvariable=var, width=width,
                      validate="focusout",
                      validatecommand=lambda i=i, key=key, arg=arg:
                      self.param_has_changed(i, key, arg))
        entry.insert(0, val)
        add(entry, row, col, padx=0, cspan=cspan)
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

    def add_entry_peak_labels(self, row, col, i):
        """ Add Tk.Entry at (row, col) linked to models_labels[i] """
        peak_label = StringVar(value=self.spectrum.peak_labels[i])
        entry = Entry(self.frame, textvariable=peak_label, width=8)
        add(entry, row, col)
        entry.bind('<Return>', lambda event, i=i: self.label_has_changed(i))
        self.peak_labels.append(peak_label)

    def add_combobox_peak_model(self, row, col, i, model):
        """ Add Tk.Combobox at (row, col) linked to peak_models[i] """
        model_name = StringVar(value=self.spectrum.get_model_name(model))
        cbox = Combobox(self.frame, values=list(PEAK_MODELS.keys()),
                        textvariable=model_name, width=15)
        add(cbox, row, col)
        cbox.bind('<<ComboboxSelected>>',
                  lambda event, i=i: self.model_has_changed(i))
        self.peak_models.append(model_name)

    def add_combobox_bkg_model(self, row, col):
        """ Add Tk.Combobox at (row, col) linked to the bkg_model """
        if self.spectrum.bkg_model is not None:
            self.bkg_name.set(self.spectrum.bkg_model.name2)
        cbox = Combobox(self.frame, values=list(BKG_MODELS.keys()),
                        textvariable=self.bkg_name, width=15)
        add(cbox, row, col)
        cbox.bind('<<ComboboxSelected>>', self.bkg_model_has_changed)

    def label_has_changed(self, i):
        """ Update the label related to the ith-model """
        self.spectrum.peak_labels[i] = self.peak_labels[i].get()
        self.plot()  # pylint:disable=not-callable
        self.update()

    def params_has_changed(self):
        for i, peak_model in enumerate(self.spectrum.peak_models):
            params = peak_model.param_hints
            for key in params.keys():
                if key in ['x0', 'ampli', 'fwhm', 'fwhm_l', 'fwhm_r']:
                    for arg in ['value', 'min', 'max']:
                        if arg in self.params[i][key]:
                            self.params[i][key][arg].set(value=params[key][arg])

    def param_has_changed(self, i, key, arg):
        """ Update the 'key'-param 'arg'-value related to the ith-model """
        if i < len(self.spectrum.peak_models):
            param = self.spectrum.peak_models[i].param_hints[key]
        else:
            param = self.spectrum.bkg_model.param_hints[key]

        value = self.params[i][key][arg].get()
        if arg == 'vary':
            value = not bool(value)
        elif arg == 'expr':
            pass
        else:  # 'value', 'min', 'max'
            value = float(value)
            if arg == 'value':
                value = max(min(param['max'], value), param['min'])
                self.params[i][key][arg].set(f'{value:.4g}')  # bound the value
        param[arg] = value
        self.spectrum.result_fit = lambda: None
        self.plot()  # pylint:disable=not-callable

    def model_has_changed(self, i):
        """ Update the model function related to the ith-model """
        spectrum = self.spectrum
        old_model_name = self.spectrum.get_model_name(spectrum.peak_models[i])
        new_model_name = self.peak_models[i].get()
        if new_model_name != old_model_name:
            ampli = spectrum.peak_models[i].param_hints['ampli']['value']
            x0 = spectrum.peak_models[i].param_hints['x0']['value']
            dx = max(np.diff(spectrum.x))
            peak_model = spectrum.create_peak_model(i + 1, new_model_name, x0=x0, ampli=ampli,
                                                    fwhm=dx, fwhm_l=dx, fwhm_r=dx)
            spectrum.peak_models[i] = peak_model
            self.spectrum.result_fit = lambda: None
            self.plot()  # pylint:disable=not-callable
            self.update()

    def bkg_model_has_changed(self, _):
        """ Update the 'bkg_model' """
        self.spectrum.set_bkg_model(self.bkg_name.get())
        self.spectrum.result_fit = lambda: None
        self.plot()  # pylint:disable=not-callable
        self.update()

    def set_header(self):
        """ Set the TabView header """
        frame = self.frame

        add(Checkbutton(frame, text='show bounds', variable=self.show_bounds,
                        command=self.update), 0, 3, W)
        add(Checkbutton(frame, text='show expressions', variable=self.show_expr,
                        command=self.update), 1, 3, W)

    def delete_models(self):
        """ Delete selected (peak) models """
        nb_models = len(self.peak_models_delete)
        for i, val in enumerate(reversed(self.peak_models_delete)):
            if val.get():
                self.spectrum.del_peak_model(nb_models - i - 1)
                self.spectrum.result_fit = lambda: None
        self.plot()  # pylint:disable=not-callable
        self.update()

    def update(self):
        """ Update the Tabview """
        self.delete()

        self.peak_models = []
        self.peak_models_delete = []
        self.peak_labels = []
        self.params = {}
        row = 3

        frame = self.frame
        spectrum = self.spectrum
        peak_models = spectrum.peak_models
        bkg_model = spectrum.bkg_model

        if len(peak_models) > 0:
            add(Button(frame, text='Del.', command=self.delete_models), 2, 0)
            add(Label(frame, text='prefix', width=5), 2, 1)
            add(Label(frame, text='labels', width=5), 2, 2)
            add(Label(frame, text='models', width=10), 2, 3)

            keys_models = [x[4:] for peak_model in peak_models
                           for x in peak_model.param_names]
            keys = []
            col = 5
            for key in PEAK_PARAMS:
                if key in keys_models:
                    label = key.replace("_l", " (left)")
                    label = label.replace("_r", " (right)")
                    add(Label(frame, text=label, width=10), 2, col)
                    keys.append(key)
                    col += 4
            for i, peak_model in enumerate(peak_models):
                self.add_model(peak_model, i, row, keys)
                row += 2

        if bkg_model is not None:
            keys = bkg_model.param_names
            for j, label in enumerate(keys):
                add(Label(frame, text=label, width=10), row, 4 * j + 5)
            row += 1
        else:
            keys = []
        add(Label(frame, text='BKG parameters', width=25), row, 0, cspan=3)
        self.add_model(bkg_model, len(peak_models), row, keys)

    def add_model(self, model, i, row, keys):
        """ Add model in the Tabview """
        if model is None:
            self.add_combobox_bkg_model(row, 3)
            return

        if model.prefix:
            var = BooleanVar(value=False)
            add(Checkbutton(self.frame, variable=var), row, 0)
            self.peak_models_delete.append(var)
            add(Label(self.frame, text=model.prefix, font='Helvetica 10 bold',
                      fg=rgb2hex(CMAP(i % CMAP.N)), width=4), row, 1)
            self.add_entry_peak_labels(row, 2, i)
            self.add_combobox_peak_model(row, 3, i, model)
        else:
            self.add_combobox_bkg_model(row, 3)

        params = model.param_hints
        self.params[i] = {}
        for k, key in enumerate(keys):
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

    def delete(self):
        """ Delete all the values contained in frames """
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.set_header()


class StatsView(ResultView):
    """ Class for fit statistics displaying """

    def __init__(self, root):
        super().__init__(root)

        vsbar = Scrollbar(self.frame, orient='vertical')
        vsbar.pack(side=RIGHT, fill='y')
        self.text = Text(self.frame, yscrollcommand=vsbar.set)
        vsbar.config(command=self.text.yview)

    def update(self):
        """ Update the statistics """
        self.text.delete(1.0, END)
        if self.spectrum is not None:
            if isinstance(self.spectrum.result_fit, ModelResult):
                self.text.insert(END, fit_report(self.spectrum.result_fit))
                self.text.pack()

    def delete(self):
        """ Delete all the values contained in frames """
        self.text.delete(1.0, END)


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
            if isinstance(val, (IntVar, DoubleVar)):
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


class FitSettings(Settings):
    """ Class for fitting parameters setting """

    def __init__(self, root):
        super().__init__(root)
        neg_value = int(FIT_PARAMS['fit_negative'])
        outliers = int(FIT_PARAMS['fit_outliers'])
        independent = int(FIT_PARAMS['independent_models'])
        self.params = {
            'fit_negative_values': StringVar(value=['Off', 'On'][neg_value]),
            'fit_outliers': StringVar(value=['Off', 'On'][outliers]),
            'independent_models': StringVar(value=['Off', 'On'][independent]),
            'coef_noise': DoubleVar(value=FIT_PARAMS['coef_noise']),
            'maximum_iterations': IntVar(value=FIT_PARAMS['max_ite']),
            'method': StringVar(value=FIT_PARAMS['method']),
            'xtol': DoubleVar(value=FIT_PARAMS['xtol']),
            'ncpus': StringVar(value=FIT_PARAMS['ncpus'])}

    def frame_creation(self, bind_fun, excluded_keys=None):
        excluded_keys = ['method', 'ncpus']
        super().frame_creation(bind_fun, excluded_keys=excluded_keys)

        count = itertools.count(start=len(self.params) - len(excluded_keys))

        k = next(count)
        add(Label(self.frame, text='method'), k, 0, E)
        add(Combobox(self.frame, values=list(FIT_METHODS.keys()),
                     textvariable=self.params['method'], width=12), k, 1, W)

        k = next(count)
        add(Label(self.frame, text='Number of CPUs'), k, 0, E)
        add(Combobox(self.frame, values=NCPUS,
                     textvariable=self.params['ncpus'], width=6), k, 1, W)


class FigureSettings(Settings):
    """ Class for figure parameters setting """

    def __init__(self, root):
        super().__init__(root)
        self.params = {'plot_fit': StringVar(value='On'),
                       'plot_negative_values': StringVar(value='On'),
                       'plot_weights': StringVar(value='Off'),
                       'plot_outliers': StringVar(value='On'),
                       'plot_outliers_limit': StringVar(value='On'),
                       'plot_noise_level': StringVar(value='On'),
                       'plot_baseline': StringVar(value='On'),
                       'plot_background': StringVar(value='On'),
                       'plot_residual': StringVar(value='Off'),
                       'coef_residual': IntVar(value=1),
                       'show_peaks_labels': StringVar(value='On'),
                       'interactive_bounds': StringVar(value='On'),
                       'x-log': StringVar(value='Off'),
                       'y-log': StringVar(value='Off'),
                       'title': StringVar(value='DEFAULT'),
                       'x_label': StringVar(value=''),
                       'y_label': StringVar(value=''),
                       }

    def frame_creation(self, bind_fun, excluded_keys=None):
        excluded_keys = ['title', 'x_label', 'y_label']
        super().frame_creation(bind_fun, excluded_keys=excluded_keys)

        count = itertools.count(start=len(self.params) - len(excluded_keys))

        add_entry(self.frame, next(count), 'title', self.params['title'],
                  width=10, bind_fun=bind_fun)

        add_entry(self.frame, next(count), 'x-label', self.params['x_label'],
                  width=10, bind_fun=bind_fun)

        add_entry(self.frame, next(count), 'y-label', self.params['y_label'],
                  width=10, bind_fun=bind_fun)


if __name__ == '__main__':
    import tkinter as tk
    from fitspy.core.spectrum import Spectrum

    models = []
    for ind in range(5):
        models.append(Spectrum.create_peak_model(ind, 'Lorentzian',
                                                 x0=100 * ind, ampli=10 * ind))

    my_spectrum = Spectrum()
    my_spectrum.peak_labels = list(range(5))
    my_spectrum.peak_models = models

    my_root = tk.Tk()
    paramsview = ParamsView(my_root)
    paramsview.hidden = True
    paramsview.spectrum = my_spectrum
    paramsview.plot = print
    paramsview.set_header()
    paramsview.update()
    paramsview.show_hide()
    my_root.mainloop()
