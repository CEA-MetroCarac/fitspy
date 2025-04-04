"""
GUI and Appli classes associated to the spectra fitting application
"""
import os
import platform
import warnings

from tkinter import (Tk, Toplevel, Frame, LabelFrame, Label, Radiobutton, Scale,
                     Entry, Text, Button, Checkbutton, messagebox, W, E, END,
                     HORIZONTAL, IntVar, DoubleVar, StringVar, BooleanVar)
from tkinter.ttk import Combobox
from tkinter import filedialog as fd
from tkinter.messagebox import askyesno
import itertools
from pathlib import Path
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

try:
    import win32clipboard
except:
    pass

from fitspy import PEAK_MODELS, BKG_MODELS, PEAK_PARAMS, SETTINGS_FNAME
from fitspy.core.utils import closest_index, save_to_json, load_from_json

from fitspy.apps.tkinter.utils import add, interactive_entry as entry
from fitspy.apps.tkinter.utils import ToggleFrame, FilesSelector, ProgressBar
from fitspy.apps.tkinter.toplevels import ParamsView, StatsView, FitSettings, FigureSettings
from fitspy.apps.tkinter.callbacks import Callbacks
from fitspy.apps import fitspy_launcher as fitspy_launcher_generic

FONT = ('Helvetica', 8, 'bold')


class GUI(Callbacks):
    """
    Gui associated to the spectra fitting application

    Attributes
    ----------
    ax_map, canvas_map: Matplotlib.Axes, FigureCanvasTkAgg
        Axes and canvas related to the 2D-map figure displaying
    figure_settings: FigureSettings obj
        Tkinter.TopLevel derivative object for figure parameters setting
    fit_settings: FitSettings obj
        Tkinter.TopLevel derivative object for fitting parameters setting
    paramsview: ParamsView obj
        Tkinter.TopLevel derivative object for fitting models params displaying
    statsview: StatsView obj
        Tkinter.TopLevel derivative object for fitting stats results displaying
    progressbar: ProgressBar obj
        Tkinter.TopLevel derivative object with progression bar
    range_min, range_max: Tkinter.StringVars
        Range associated to the spectrum support
    outliers_coef: Tkinter.DoubleVar
        Coefficient applied to the outliers limits
    baseline_mode: Tkinter.StringVar
        Method associated with the baseline determination method ('Semi-Auto',
        'Linear' or 'Polynomial')
    baseline_coef: Tkinter.IntVar
        Smoothing coefficient used when calculating the baseline with the
        'Semi-Auto' algorithm
    baseline_attached: Tkinter.BooleanVar
        Activation keyword for baseline points attachment to the spectra
    baseline_sigma: Tkinter.IntVar
        Smoothing gaussian coefficient applied to the spectra when calculating
        the attached baseline points
    baseline_distance: Tkinter.DoubleVar
        Minimum distance used by 'spectrum.auto_baseline'
    baseline_mode: Tkinter.StringVar
        Type of baseline ('Linear' or 'Polynomial')
    baseline_order_max: Tkinter.IntVar
        Max polynomial order to consider when plotting/removing the baseline
    normalize: Tkinter.BooleanVar
        Activation keyword for spectrum profiles normalization
    normalize_range_min, normalize_range_max: Tkinter.StringVars
        Ranges for searching the maximum value used in the normalization
    model: Tkinter.StringVar
        Spectrum peak base model name among 'Gaussian', 'Lorentzian',
        'GaussianAsym' and 'LorentzianAsym'
    bkg_name: Tkinter.StringVar
        Background model name among 'None', 'Constant', 'Linear', 'Parabolic'
        and 'Exponential'
    asym: Tkinter.BooleanVar
        Activation keyword to consider asymetric spectrum model
    ax: Matplotlib.Axes object
        Current axis to work with
    canvas: FigureCanvasTkAgg object
        Current canvas to work with
    fileselector: common.core.appli_gui.FilesSelector object
        Widget dedicated to the files selection
    """

    def __init__(self):
        super().__init__()

        # TopLevels linked to the application
        self.figure_settings = FigureSettings(self.root)
        self.fit_settings = FitSettings(self.root)
        self.paramsview = ParamsView(self.root)
        self.statsview = StatsView(self.root)

        # Spectrum parameters
        self.range_min = DoubleVar()
        self.range_max = DoubleVar()
        self.outliers_coef = DoubleVar(value=1.5)

        # Baseline parameters
        self.baseline_attached = BooleanVar(value=True)
        self.baseline_sigma = IntVar(value=0)
        self.baseline_distance = IntVar(value=500)
        self.baseline_mode = StringVar(value="Semi-Auto")
        self.baseline_coef = IntVar(value=5)
        self.baseline_order_max = IntVar(value=2)

        # normalization parameters
        self.normalize = BooleanVar(value=False)
        self.normalize_range_min = StringVar(value="")
        self.normalize_range_max = StringVar(value="")

        # Peaks parameters
        self.model = StringVar(value='Lorentzian')
        self.bkg_name = StringVar(value='None')
        self.asym = BooleanVar(value=False)

        # Frames creation
        #################

        frame = Frame(self.root)

        frame_visu = Frame(frame)
        frame_visu.grid(row=0, column=0, sticky=W + E)

        frame_proc = Frame(frame)
        frame_proc.grid(row=0, column=1, padx=0, sticky=W + E)

        frame.pack()

        # VISU frame
        ############

        add(Button(frame_visu, text='Figure settings',
                   command=self.update_figure_settings), 0, 0)

        fig, self.ax = plt.subplots(figsize=(12, 8.8))
        self.canvas = FigureCanvasTkAgg(fig, master=frame_visu)
        self.canvas.get_tk_widget().grid(row=1, column=0)
        self.canvas.draw()

        def clipboard_handler(event):
            """ Put the current figure in the clipboard, for Copy/Paste,
            inspired from: https://github.com/joshburnett/addcopyfighandler """
            if event.key == 'ctrl+c' and platform.system().lower() == 'windows':
                with BytesIO() as buf:
                    fig.savefig(buf, format='png')
                    data = buf.getvalue()

                format_id = win32clipboard.RegisterClipboardFormat('PNG')
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(format_id, data)
                win32clipboard.CloseClipboard()

        self.canvas.mpl_connect('key_press_event', clipboard_handler)

        fr_toolbar = Frame(frame_visu)
        fr_toolbar.grid(row=2, column=0, sticky=W, pady=0)
        toolbar = NavigationToolbar2Tk(self.canvas, fr_toolbar)
        toolbar._buttons['Home'].bind("<Button-1>", lambda x: self.rescale())

        self.preserve_axis = BooleanVar(value=False)
        add(Checkbutton(frame_visu, variable=self.preserve_axis,
                        text='Preserve axis'), 2, 0)
        self.subtract_baseline_bkg = BooleanVar(value=True)
        add(Checkbutton(frame_visu, variable=self.subtract_baseline_bkg,
                        text='Subtract baseline+background', command=self.plot), 2, 0, E)
        # FILES SELECTION frame
        #######################

        fr = Frame(frame_proc)
        row = itertools.count()

        add(fr, next(row), 0, W + E)

        self.fileselector = FilesSelector(root=fr, lbox_size=[45, 9])
        self.fileselector.lbox.bind('<<ListboxSelect>>', self.update)
        self.fileselector.lbox.bind('<<ListboxAdd>>', self.add_items)
        self.fileselector.lbox.bind('<<ListboxRemove>>', self.delete)
        self.fileselector.lbox.bind('<<ListboxRemoveAll>>', self.delete_all)

        # SPECTRA PROCESSING frame
        ##########################

        fr = Frame(frame_proc)
        add(fr, next(row), 0, W + E)

        add(Button(fr, text="Show All", command=self.show_all), 0, 0)
        add(Button(fr, text="Auto eval", command=self.auto_eval), 0, 1)
        add(Button(fr, text="Auto eval All", command=self.auto_eval_all), 0, 2)
        add(Button(fr, text="Save Settings", command=self.save_settings), 1, 0)
        add(Button(fr, text="Reinitialize", command=self.reinit), 1, 1)
        add(Button(fr, text="Reinitialize All", command=self.reinit_all), 1, 2)

        # Overall parameters

        fr = LabelFrame(frame_proc, text="Overall settings", font=FONT)
        add(fr, next(row), 0, W + E)
        add(Label(fr, text='X-range :'), 0, 0)
        entry_min = Entry(fr, textvariable=self.range_min, w=9)
        entry_max = Entry(fr, textvariable=self.range_max, w=9)
        entry_min.bind("<Return>", lambda event: self.apply_range())
        entry_max.bind("<Return>", lambda event: self.apply_range())
        add(entry_min, 0, 1)
        add(entry_max, 0, 2)
        add(Button(fr, text="Apply to all",
                   command=self.apply_range_to_all), 0, 3)

        add(Button(fr, text='Outliers Calc.',
                   command=self.outliers_calculation), 2, 0, E, cspan=2)
        add(Label(fr, text='coef :'), 2, 2, E)
        entry_outliers_coef = Entry(fr, textvariable=self.outliers_coef, w=3)
        entry_outliers_coef.bind("<Return>", lambda _: self.set_outliers_coef())
        add(entry_outliers_coef, 2, 3, W)

        # Baseline

        self.fr_baseline = ToggleFrame(frame_proc, text='Baseline', font=FONT)
        add(self.fr_baseline, next(row), 0, W + E)

        fr = self.fr_baseline

        var_mode = self.baseline_mode
        var_coef = self.baseline_coef
        modes = ["Semi-Auto", "Linear", "Polynomial"]
        texts = ["Semi-Auto :", "Linear", "Polynomial - Order :"]
        add(Radiobutton(fr, text=texts[0], variable=var_mode, value=modes[0],
                        command=self.apply_baseline_settings), 0, 0)
        scale = Scale(fr, variable=var_coef, from_=0, to=10, showvalue=False,
                      orient=HORIZONTAL)
        scale.bind("<ButtonRelease-1>",
                   lambda _: self.apply_baseline_settings())
        add(scale, 0, 1, W)

        add(Button(fr, text="Import", command=self.load_baseline), 0, 2)
        add(Radiobutton(fr, text=texts[1], variable=var_mode, value=modes[1],
                        command=self.apply_baseline_settings), 1, 0)
        add(Radiobutton(fr, text=texts[2], variable=var_mode, value=modes[2],
                        command=self.apply_baseline_settings), 1, 1)
        order_entry = Entry(fr, textvariable=self.baseline_order_max, width=2)
        add(order_entry, 1, 2, W)
        order_entry.bind("<KeyRelease>", lambda _: self.apply_baseline_settings())

        add(Checkbutton(fr, variable=self.baseline_attached, text='Attached',
                        command=self.apply_baseline_settings), 2, 0)
        add(Label(fr, text="Sigma (smoothing) :"), 2, 1, E)
        sigma_entry = Entry(fr, textvariable=self.baseline_sigma, width=4)
        add(sigma_entry, 2, 2, W)
        sigma_entry.bind("<KeyRelease>", lambda _: self.apply_baseline_settings())

        add(Button(fr, text="Apply to All",
                   command=self.apply_baseline_settings_to_all), 3, 1, W)

        self.fr_baseline.enable()
        self.fr_baseline.bind("<Button-1>", self.on_press_baseline_peaks)

        # Normalization

        fr = LabelFrame(frame_proc, text="Normalization", font=FONT)
        add(fr, next(row), 0, W + E)

        add(Checkbutton(fr, text='Normalize', variable=self.normalize,
                        command=self.update_normalize), 0, 0, E)
        add(Label(fr, text='X-range :'), 0, 1)
        entry_min = Entry(fr, textvariable=self.normalize_range_min, w=9)
        entry_max = Entry(fr, textvariable=self.normalize_range_max, w=9)
        entry_min.bind("<Return>", lambda event: self.update_normalize_range())
        entry_max.bind("<Return>", lambda event: self.update_normalize_range())
        add(entry_min, 0, 2)
        add(entry_max, 0, 3)

        # Fitting

        self.fr_fit = ToggleFrame(frame_proc, text='Fitting', font=FONT)
        add(self.fr_fit, next(row), 0, W + E)

        fr = self.fr_fit

        def update_cbox(cbox, models):
            cbox['value'] = list(models.keys())

        add(Label(fr, text='Peak model :'), 0, 0, E)
        cbox1 = Combobox(fr, values=list(PEAK_MODELS.keys()),
                         postcommand=lambda: update_cbox(cbox1, PEAK_MODELS),
                         textvariable=self.model, width=16)
        add(cbox1, 0, 1, cspan=2)
        add(Button(fr, text="Load",
                   command=lambda: self.load_user_model('PEAK_MODELS')), 0, 3)

        add(Label(fr, text='BKG model :'), 1, 0, E)
        cbox2 = Combobox(fr, values=list(BKG_MODELS.keys()),
                         postcommand=lambda: update_cbox(cbox2, BKG_MODELS),
                         textvariable=self.bkg_name, width=16)
        add(cbox2, 1, 1, cspan=2)
        cbox2.bind('<<ComboboxSelected>>',
                   lambda _: self.set_bkg_model())
        add(Button(fr, text="Load",
                   command=lambda: self.load_user_model('BKG_MODELS')), 1, 3)

        add(Button(fr, text="Parameters",
                   command=lambda: self.show_hide_results('params')), 2, 0)
        add(Button(fr, text="Stats",
                   command=lambda: self.show_hide_results('stats')), 2, 1)
        add(Button(fr, text='Auto', command=self.auto_peaks), 2, 2)
        add(Button(fr, text='Fit Settings',
                   command=self.update_fit_settings), 2, 3)

        add(Button(fr, text=" Fit Selec.", command=self.fit), 3, 0)
        add(Button(fr, text=" Fit All ", command=self.fit_all), 3, 1)
        add(Button(fr, text="Remove", command=self.remove), 3, 2)
        add(Button(fr, text="Save Results", command=self.save_results), 3, 3)

        self.fr_fit.disable()
        self.fr_fit.bind("<Button-1>", self.on_press_baseline_peaks)

        # Models : saving/reloading

        fr = LabelFrame(frame_proc, text='Models', font=FONT)
        add(fr, next(row), 0, W + E)

        add(Button(fr, text="Save Selec.", command=self.save_selection), 0, 0)
        add(Button(fr, text="Save All", command=self.save_all), 0, 1)
        add(Button(fr, text="Reload", command=self.reload), 0, 2)

        add(Button(fr, text="Load Model",
                   command=self.load_model), 1, 0, padx=9)
        add(Button(fr, text="Apply to Selec.",
                   command=self.apply_model), 1, 1, padx=9)
        add(Button(fr, text="Apply to All",
                   command=self.apply_model_to_all), 1, 2, padx=9)

        add(Label(fr, text='Loaded model :'), 2, 0)
        self.text_model = Text(fr, height=1, width=20)
        add(self.text_model, 2, 1, cspan=2)

        # Add ProgressBar

        fr = Frame(frame_proc)
        add(fr, next(row), 0, W + E)
        self.progressbar = ProgressBar(fr)

        self.reload_settings()

    def frame_map_creation(self, spectra_map):
        """ Create a frame_map Tkinter.Toplevel() and related 'ax' and 'canvas'
            as spectra_map attributes """
        frame_map = Toplevel(self.root)
        frame_map.title(os.path.basename(spectra_map.fname))
        frame_map.protocol("WM_DELETE_WINDOW", lambda *args: None)

        # attach tkinter objects to spectra_map
        keys = ['Intensity (sum)'] + PEAK_PARAMS
        vmin = np.nanmin(spectra_map.arr)
        vmax = np.nanmax(spectra_map.arr)
        setattr(spectra_map, 'var', StringVar(value=keys[0]))
        setattr(spectra_map, 'label', StringVar(value=''))
        setattr(spectra_map, 'vmin', DoubleVar(value=vmin))
        setattr(spectra_map, 'vmax', DoubleVar(value=vmax))

        def update_labels():
            labels = sorted(list(set([label for spectrum in spectra_map
                                      for label in spectrum.peak_labels])))
            cbox1['values'] = labels
            if len(labels) > 0:
                spectra_map.label.set(labels[0])

        def update_var():
            if "Intensity" in spectra_map.var.get():
                spectra_map.ax_slider.set_visible(True)
                label1.grid_forget()
                cbox1.grid_forget()
            else:
                spectra_map.ax_slider.set_visible(False)
                label1.grid(row=1, column=0, sticky=W)
                cbox1.grid(row=1, column=1, padx=5)
            update_map()

        def update_map(vmin=None, vmax=None):
            spectra_map.plot_map_update(var=spectra_map.var.get(),
                                        label=spectra_map.label.get(),
                                        vmin=vmin, vmax=vmax)
            if vmin is None and vmax is None:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    spectra_map.vmin.set(np.nanmin(spectra_map.arr))
                    spectra_map.vmax.set(np.nanmax(spectra_map.arr))

        def export_to_csv():
            fname = str(Path(spectra_map.fname).stem)
            var = spectra_map.var.get().split()[0]
            if var == "Intensity":
                fname += "_intensity.csv"
            else:
                fname += f"_{var}_{spectra_map.label.get()}.csv"

            fname_csv = fd.asksaveasfilename(defaultextension='.csv',
                                             initialfile=fname)

            if fname_csv == '':
                return
            if not os.path.isfile(fname_csv):
                msg = f'{Path(fname_csv).name} already exists.\n'
                msg += 'Do you want to overwrite it?'.center(24)
                if not askyesno('', msg):
                    return
            spectra_map.export_to_csv(fname_csv)

        frame = Frame(frame_map)
        frame.grid(row=0, column=0)
        add(Label(frame, text="              "), 0, 0)  # permanent blank label
        cbox0 = Combobox(frame, values=keys, textvariable=spectra_map.var, w=14)
        add(cbox0, 0, 1, W)
        cbox0.bind('<<ComboboxSelected>>', lambda _: update_var())

        add(Label(frame, text="min:"), 0, 2, E)
        entmin = Entry(frame, textvariable=spectra_map.vmin, w=9)
        add(entmin, 0, 3, W)
        entmin.bind("<KeyRelease>",
                    lambda _: update_map(vmin=spectra_map.vmin.get(),
                                         vmax=spectra_map.vmax.get()))

        add(Label(frame, text="max:"), 0, 4, E)
        entmax = Entry(frame, textvariable=spectra_map.vmax, w=9)
        add(entmax, 0, 5, W)
        entmax.bind("<KeyRelease>",
                    lambda _: update_map(vmin=spectra_map.vmin.get(),
                                         vmax=spectra_map.vmax.get()))

        add(Button(frame, text='Export\n(.csv)', width=14,
                   command=export_to_csv), 0, 6, rspan=2)

        add(Label(frame, text="              "), 1, 0)  # permanent blank label
        label1 = Label(frame, text="       Label:")
        cbox1 = Combobox(frame, textvariable=spectra_map.label, width=14,
                         postcommand=update_labels)
        cbox1.bind('<<ComboboxSelected>>', lambda _: update_map())

        fig, ax = plt.subplots(figsize=(6.5, 5))
        canvas = FigureCanvasTkAgg(fig, master=frame_map)
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=2)
        canvas.draw()

        # attach objects to spectra_map
        spectra_map.ax = ax
        setattr(spectra_map, 'frame', frame_map)
        setattr(spectra_map, 'canvas', canvas)
        setattr(spectra_map, 'marker', None)

        def on_press(event):
            ax = spectra_map.ax
            if event.inaxes == ax:

                xy_map = spectra_map.xy_map
                fnames = self.fileselector.filenames

                # update marker
                if spectra_map.marker is not None:
                    [x.remove() for x in spectra_map.marker]
                x = xy_map[0][closest_index(xy_map[0], event.xdata)]
                y = xy_map[1][closest_index(xy_map[1], event.ydata)]
                spectra_map.marker = ax.plot(x, y, 'rs', ms=9, mfc='none')
                ax.set_xlim(spectra_map.extent[0], spectra_map.extent[1])
                ax.set_ylim(spectra_map.extent[2], spectra_map.extent[3])
                spectra_map.canvas.draw()

                # update spectrum
                fname = f"{spectra_map.fname}  X={x}  Y={y}"
                if fname in fnames:
                    ind = fnames.index(fname)
                    self.update(fname)
                    self.fileselector.lbox.selection_clear(0, END)
                    self.fileselector.lbox.selection_set(ind)
                    cursor_position = ind / len(fnames)
                    self.fileselector.lbox.yview_moveto(cursor_position)
                    self.fileselector.lbox.update()
                else:
                    self.ax.clear()
                    self.canvas.draw()

        spectra_map.canvas.mpl_connect('button_press_event', on_press)

    def save_settings(self):
        """ Save GUI users settings """
        dict_attrs = {}
        for key, val in vars(self).items():
            if isinstance(val, (BooleanVar, IntVar, StringVar)):
                dict_attrs[key] = val.get()
        for pfx in ['fit', 'figure']:
            key = f"{pfx}_settings"
            dict_attrs[key] = {}
            obj = eval(f"self.{key}")
            for key2, val2 in obj.params.items():
                dict_attrs[key][key2] = val2.get()
        save_to_json(SETTINGS_FNAME, dict_attrs)

    def reload_settings(self):
        """ Reload GUI users settings """
        if SETTINGS_FNAME.is_file():
            dict_attrs = load_from_json(SETTINGS_FNAME)
            for key, val in dict_attrs.items():
                # try/except to manage changes in attributes
                try:
                    if isinstance(val, dict):
                        obj = eval(f"self.{key}")
                        for key2, val2 in val.items():
                            obj.params[key2].set(val2)
                    else:
                        var = getattr(self, key)
                        var.set(val)
                except AttributeError:
                    pass
        self.baseline_mode.set(None)


class Appli(GUI):
    """
    Application for spectra fitting

    Attributes
    ----------
    root: Tkinter.Tk object
        Root window
    force_terminal_exit: bool
        Key to force terminal session to exit after 'root' destroying
    """

    def __init__(self, root, size="1550x950", force_terminal_exit=True):
        root.title("Fitspy")
        root.geometry(size)
        self.root = root
        self.force_terminal_exit = force_terminal_exit
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        super().__init__()

    @property
    def fnames(self):
        return self.spectra.fnames

    def on_closing(self):
        """ To quit 'properly' the application """
        if messagebox.askokcancel("Quit", "Would you like to quit ?"):
            self.root.destroy()


def init_app():
    """ Return an Appli and Tk instances """
    root = Tk()
    appli = Appli(root)
    return appli, root


def end_app(appli, root, dirname_res=None):
    """ Quit properly the appli after saving the results if 'dirname_res' is given (for pytest) """
    if dirname_res is not None:
        appli.save_results(dirname_res=dirname_res)
        root.destroy()
        return
    else:
        root.mainloop()


def fitspy_launcher(fname_json=None):
    """ Launch the Tkinter appli """
    fitspy_launcher_generic(fname_json=fname_json, gui='tkinter')


if __name__ == '__main__':
    fitspy_launcher()
