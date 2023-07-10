"""
GUI and Appli classes associated to the spectra fitting application
"""
import os

from tkinter import (Tk, Toplevel, Frame, LabelFrame, Label, Radiobutton,
                     Entry, Text, Button, Checkbutton, W, E, END,
                     IntVar, DoubleVar, StringVar, BooleanVar)
from tkinter.ttk import Combobox
import itertools
from pathlib import Path
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

try:
    import win32clipboard
except:
    pass

from fitspy.utils import closest_index, save_to_json, load_from_json
from fitspy.spectra import MODELS, BKG_MODELS

from fitspy.app.utils import add, interactive_entry
from fitspy.app.utils import ToggleFrame, ScrollbarFrame, FilesSelector
from fitspy.app.toplevels import TabView
from fitspy.app.toplevels import AttractorsSettings, FitSettings
from fitspy.app.toplevels import FigureSettings
from fitspy.app.callbacks import Callbacks, FIT_METHODS

SETTINGS_PATHNAME = Path.home() / Path(".fitspy.json")
FONT = ('Helvetica', 8, 'bold')


class GUI(Callbacks):
    """
    Gui associated to the spectra fitting application

    Attributes
    ----------
    frame_map: Tkinter.TopLevel
        Frame used to display the 2D-map field (integrated spectrum intensities)
    ax_map, canvas_map: Matplotlib.Axes, FigureCanvasTkAgg
        Axes and canvas related to the 2D-map figure displaying
    figure_settings: FigureSettings obj
        Tkinter.TopLevel derivative object for figure parameters setting
    attractors_settings: AttractorsSettings obj
        Tkinter.TopLevel derivative object for attractors parameters setting
    fit_settings: FitSettings obj
        Tkinter.TopLevel derivative object for fitting parameters setting
    tabview: TabView obj
        Tkinter.TopLevel derivative object for fitting results models displaying
    range_min, range_max: Tkinter.DoubleVars
        Range associated to the spectrum support
    normalize_mode: Tkinter.StringVar
        Type of normalization ('Maximum' or 'Attractor')
    attractor_position: Tkinter.IntVar
        Reference position in case of 'Attractor' normalize_mode
    attractors: Tkinter.BooleanVar
        Activation keyword for spectrum peaks association when adding
    attached: Tkinter.BooleanVar
        Activation keyword for baseline points attachment to the spectra
    sigma: Tkinter.IntVar
        Smoothing gaussian coefficient applied to the spectra when calculating
        the attached baseline points
    distance: Tkinter.DoubleVar
        Minimum distance used by 'spectrum.auto_baseline'
    baseline_mode: Tkinter.StringVar
        Type of baseline ('Linear' or 'Polynomial')
    baseline_order_max: Tkinter.IntVar
        Max polynomial order to consider when plotting/removing the baseline
    model: Tkinter.StringVar
        Spectrum peak base model name among 'Gaussian', 'Lorentzian',
        'GaussianAsym' and 'LorentzianAsym'
    bkg_model: Tkinter.StringVar
        Background model name among 'None', 'Constant', 'Linear', 'Parabolic',
        'Gaussian' and 'Exponential'
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
        self.attractors_settings = AttractorsSettings(self.root)
        self.fit_settings = FitSettings(self.root)
        self.tabview = TabView(self.root)

        # Spectrum parameters
        self.range_min = DoubleVar(value=-1)
        self.range_max = DoubleVar(value=99999)
        self.attractors = BooleanVar(value=True)

        # Baseline parameters
        self.attached = BooleanVar(value=True)
        self.sigma = IntVar(value=0)
        self.distance = DoubleVar(value=500)
        self.baseline_mode = StringVar(value='Linear')
        self.baseline_order_max = IntVar(value=2)

        # normalization parameters
        self.normalize_mode = StringVar(value='Maximum')
        self.attractor_position = IntVar(value=-1)

        # Peaks parameters
        self.model = StringVar(value='Lorentzian')
        self.bkg_model = StringVar(value='None')
        self.asym = BooleanVar(value=False)

        # Frames creation
        #################

        frame = Frame(self.root)

        frame_visu = Frame(frame, width=700)
        frame_visu.grid(row=0, column=0, rowspan=2)

        frame_files = Frame(frame)
        frame_files.grid(row=0, column=1)

        frame_proc = Frame(frame, width=300)
        frame_proc.grid(row=1, column=1, padx=0, sticky=W + E)

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
            if event.key == 'ctrl+c' and os.system().lower() == 'windows':
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

        add(Button(frame_visu, text="Save All (.png)",
                   command=self.save_figures), 2, 0)

        # FILES SELECTION frame
        #######################

        self.fileselector = FilesSelector(root=frame_files, lbox_size=[50, 9])
        self.fileselector.lbox[0].bind('<<ListboxSelect>>', self.update)
        self.fileselector.lbox[0].bind('<<ListboxAdd>>', self.add_items)
        self.fileselector.lbox[0].bind('<<ListboxRemove>>', self.delete)
        self.fileselector.lbox[0].bind('<<ListboxRemoveAll>>', self.delete_all)

        # SPECTRA PROCESSING frame
        ##########################

        fr = Frame(frame_proc)
        fr.grid(row=0, column=0, padx=5, pady=0)

        add(Button(fr, text="Show All", command=self.show_all), 0, 0)
        add(Button(fr, text="Auto eval", command=self.auto_eval), 0, 1)
        add(Button(fr, text="Auto eval All", command=self.auto_eval_all), 0, 2)
        add(Button(fr, text="Save Settings", command=self.save_settings), 1, 0)
        add(Button(fr, text="Reinitialize", command=self.reinit), 1, 1)
        add(Button(fr, text="Reinitialize All", command=self.reinit_all), 1, 2)

        sbar = ScrollbarFrame(frame_proc, orientation='vertical')
        add(frame_proc, 1, 1, W + E)
        frame_proc_sbar = sbar.frame
        row = itertools.count()

        # Overall parameters

        fr = LabelFrame(frame_proc_sbar, text="Overall settings", font=FONT)
        add(fr, next(row), 0, W + E)
        add(Label(fr, text='X-range :'), 0, 0)
        entry_min = Entry(fr, textvariable=self.range_min, w=9)
        entry_max = Entry(fr, textvariable=self.range_max, w=9)
        entry_min.bind("<Return>", lambda event: self.set_spectrum_range())
        entry_max.bind("<Return>", lambda event: self.set_spectrum_range())
        add(entry_min, 0, 1)
        add(entry_max, 0, 2)
        add(Button(fr, text="Apply to all",
                   command=self.apply_range_to_all), 0, 3)

        add(Checkbutton(fr, text='Attractors', variable=self.attractors,
                        command=self.update_attractors), 1, 0, cspan=2)
        add(Button(fr, text='Attractors Settings',
                   command=self.update_attractors_settings), 1, 2, cspan=2)

        # Baseline

        self.fr_baseline = ToggleFrame(frame_proc_sbar, text='Baseline',
                                       font=FONT)
        add(self.fr_baseline, next(row), 0, W + E)

        fr = self.fr_baseline
        add(Button(fr, text="Import", command=self.load_baseline), 0, 0)
        add(Button(fr, text="Auto", command=self.auto_baseline), 0, 1, W)
        add(Label(fr, text="Min distance :"), 0, 1, E)
        add(Entry(fr, textvariable=self.distance, width=4), 0, 2, W)

        add(Checkbutton(fr, variable=self.attached, text='Attached',
                        command=self.plot), 1, 0)
        add(Label(fr, text="Sigma (smoothing) :"), 1, 1, E)
        add(interactive_entry(fr, self.sigma, self.plot, width=4), 1, 2, W)

        var_mode = self.baseline_mode
        var_order = self.baseline_order_max
        modes = ["Linear", "Polynomial"]
        texts = ["Linear", "Polynomial - Order :"]
        add(Radiobutton(fr, text=texts[0], variable=var_mode, value=modes[0],
                        command=self.plot), 2, 0)
        add(Radiobutton(fr, text=texts[1], variable=var_mode, value=modes[1],
                        command=self.plot), 2, 1)
        order_entry = Entry(fr, textvariable=var_order, width=2)
        add(order_entry, 2, 2, W)
        order_entry.bind("<KeyRelease>", lambda event: self.plot())

        add(Button(fr, text="Substract",
                   command=self.substract_baseline), 4, 0, padx=10)
        add(Button(fr, text="Substract All",
                   command=self.substract_baseline_to_all), 4, 1)
        add(Button(fr, text="Delete",
                   command=self.delete_baseline), 4, 2)

        self.fr_baseline.enable()
        self.fr_baseline.bind("<Button-1>", self.on_press_baseline_peaks)

        # Normalization

        fr = LabelFrame(frame_proc_sbar, text="Normalization", font=FONT)
        add(fr, next(row), 0, W + E)

        var = self.normalize_mode
        vals = ["Maximum", "Attractor near :"]
        add(Radiobutton(fr, text=vals[0], variable=var, value=vals[0]), 0, 0)
        add(Radiobutton(fr, text=vals[1], variable=var, value=vals[1]), 0, 1, E)
        add(Entry(fr, textvariable=self.attractor_position, width=8), 0, 2, W)
        add(Button(fr, text="Apply to all",
                   command=self.normalize), 1, 0, cspan=3)

        # Peaks fitting

        self.fr_peaks = ToggleFrame(frame_proc_sbar, text='Peaks', font=FONT)
        add(self.fr_peaks, next(row), 0, W + E)

        fr = self.fr_peaks
        add(Button(fr, text='Auto', command=self.auto_peaks), 0, 0)
        add(Button(fr, text='Fit Settings',
                   command=self.update_fit_settings), 0, 1, cspan=2)

        add(Label(fr, text='Peak model :'), 1, 0, E)
        add(Combobox(fr, values=list(MODELS.keys()), textvariable=self.model,
                     width=28), 1, 1, cspan=2)
        add(Label(fr, text='BKG model :'), 2, 0, E)
        add(Combobox(fr, values=BKG_MODELS, textvariable=self.bkg_model,
                     width=28), 2, 1, cspan=2)

        add(Button(fr, text=" Fit ", command=self.fit), 3, 0)
        add(Button(fr, text=" Fit All ", command=self.fit_all), 3, 1)
        add(Button(fr, text="Remove", command=self.remove), 3, 2)

        add(Button(fr, text="Parameters (Show/Hide)",
                   command=self.show_hide_results), 4, 0, cspan=2)
        add(Button(fr, text="Save (.csv)",
                   command=self.save_results), 4, 2)

        self.fr_peaks.disable()
        self.fr_peaks.bind("<Button-1>", self.on_press_baseline_peaks)

        # Models : saving/reloading

        fr = LabelFrame(frame_proc_sbar, text='Models', font=FONT)
        add(fr, next(row), 0, W + E)

        add(Button(fr, text="Save Selec.", command=self.save_selection), 0, 0)
        add(Button(fr, text="Save All", command=self.save_all), 0, 1)
        add(Button(fr, text="Reload", command=self.reload), 0, 2)

        add(Button(fr, text="Load Model",
                   command=self.load_model), 1, 0, padx=9)
        add(Button(fr, text="Apply to Sel.",
                   command=lambda: self.apply_model(selection=1)), 1, 1, padx=9)
        add(Button(fr, text="Apply to All",
                   command=lambda: self.apply_model(selection=0)), 1, 2, padx=9)

        add(Label(fr, text='Loaded model :'), 2, 0)
        self.text_model = Text(fr, height=1, width=20)
        add(self.text_model, 2, 1, cspan=2)

        sbar.update_and_resize(320, 646)

        self.reload_settings()

    def frame_map_creation(self, spectra_map):
        """ Create a frame_map Tkinter.Toplevel() and related 'ax' and 'canvas'
            as spectra_map attributes """

        frame_map = Toplevel(self.root)
        frame_map.title(os.path.basename(spectra_map.fname))
        # frame_map.protocol("WM_DELETE_WINDOW", lambda *args: None)

        fig, ax = plt.subplots(figsize=(6.5, 5))
        # marker = ax.plot(0, 0, 'rs', ms=9, mfc='none')
        canvas = FigureCanvasTkAgg(fig, master=frame_map)
        canvas.get_tk_widget().grid(row=0, column=0)
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
                fnames = self.fileselector.filenames[0]

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
                    self.fileselector.lbox[0].selection_clear(0, END)
                    self.fileselector.lbox[0].selection_set(ind)
                    cursor_position = ind / len(fnames)
                    self.fileselector.lbox[0].yview_moveto(cursor_position)
                    self.fileselector.lbox[0].update()
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
        for pfx in ['attractors', 'fit', 'figure']:
            key = f"{pfx}_settings"
            dict_attrs[key] = {}
            obj = eval(f"self.{key}")
            for key2, val2 in obj.params.items():
                dict_attrs[key][key2] = val2.get()
        save_to_json(SETTINGS_PATHNAME, dict_attrs)

    def reload_settings(self):
        """ Reload GUI users settings """
        if SETTINGS_PATHNAME.is_file():
            dict_attrs = load_from_json(SETTINGS_PATHNAME)
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


class Appli(GUI):
    """
    Application for spectra fitting

    Attributes
    ----------
    root: Tkinter.Tk object
        Root window
    """

    def __init__(self, root, size="1550x950"):
        root.title("Fitspy")
        root.geometry(size)
        self.root = root

        super().__init__()


def fitspy_launcher(fname_json=None):
    """ Launch the appli """

    root = Tk()
    appli = Appli(root)

    if fname_json is not None:
        appli.reload(fname_json=fname_json)

    root.mainloop()


if __name__ == '__main__':
    fitspy_launcher()
