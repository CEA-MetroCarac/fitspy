"""
Callback functions encapsulated in a class to interact with the GUI
"""
import os
import warnings
from tkinter import END
from tkinter.messagebox import askyesno, showerror
from tkinter import filedialog as fd
from threading import Thread
import glob
from pathlib import Path
from copy import deepcopy
import numpy as np
import matplotlib.cm as cm

from fitspy.core.spectra import Spectra
from fitspy.core.spectrum import Spectrum
from fitspy.core.spectra_map import SpectraMap
from fitspy.core.utils import get_dim, closest_index, check_or_rename
from fitspy.core.utils import load_models_from_txt, load_models_from_py
from fitspy.apps.interactive_bounds import InteractiveBounds

from . import CMAP


# TODO : change 'fit_params' from spectrum to spectra attribute (?)
# TODO : (GUI) remove 'ncpus' from the fit settings
# TODO : manage callbacks when no files have been loaded
# TODO : enable remove() with curselection()
# TODO : auto_eval() with multiprocessing capabilities
# TODO : A single 'Apply All' for all the settings


class Callbacks:
    """
    Callback functions to interact with the GUI of the spectra fitting appli

    Attributes
    ----------
    spectra: Spectra object
        List that contains all Spectrum objects
    current_spectrum: Spectrum object
        The current selected spectrum to work with
    cids: list of ints
        connection ids that can be used with FigureCanvasBase.mpl_disconnect
    show_plot: bool
        Activation key for (re)plotting
    lines: list of Matplotlib.Lines2D
        Lines related to all the spectra displaying
    nearest_lines: list Matplotlib.Lines2D
        The nearest profiles of the mouse position when clicking (limited to 10)
    tmp: matplotlib.text.Annotation
        Annotation to display fit parameters in the plot
    selected_frame: str
        Frame to enable between 'Baseline' and 'Peaks'
    model: dict
        Dictionary issued from a .json model reloading
    ncpus: int or str
        Number of CPUs to work with in fitting.
        If ncpus = "auto", determine automatically this number according to the
        number of spectra to handle and the number of available CPUs.
        if ncpus is None (default value), consider the value passed through
        fit_settings.params['ncpus']
    """

    def __init__(self):

        self.spectra = Spectra()
        self.current_spectrum = None
        self.cids = []
        self.show_plot = True
        self.is_show_all = False
        self.lines = None
        self.nearest_lines = []
        self.tmp = None
        self.selected_frame = "Baseline"
        self.model_dict = None
        self.ncpus = None

    def update_figure_settings(self):
        """ Update figure settings """
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        bind_fun = self.show_all if self.is_show_all else self.plot
        self.figure_settings.update(x, y, bind_fun=bind_fun)

    def rescale(self):
        """ Rescale the figure """
        self.ax.autoscale()
        self.canvas.draw()
        self.canvas.toolbar.update()

    def outliers_calculation(self):
        """ Calculate the outliers (limit) """
        coef = float(self.outliers_coef.get())
        self.spectra.outliers_limit_calculation(coef=coef)
        if self.is_show_all:
            self.show_all()
        else:
            self.plot()

    def set_outliers_coef(self):
        """ Set the outliers coefficient """
        self.spectra.outliers_coef = float(self.outliers_coef.get())
        self.outliers_calculation()

    def show_all(self):
        """ Show all spectra and highlight spectrum on mouse over """
        self.is_show_all = True

        fselector = self.fileselector

        xlim, ylim = self.ax.get_xlim(), self.ax.get_ylim()
        self.ax.clear()

        # reassign previous axis limits (related to zoom)
        if not xlim == ylim == (0.0, 1.0):
            self.ax.set_xlim(xlim)
            self.ax.set_ylim(ylim)

        self.lines = []
        for spectrum in self.spectra.all:
            x0, y0 = spectrum.x0, spectrum.y0
            self.lines.append(self.ax.plot(x0, y0, 'k-', lw=0.2, zorder=0)[0])
            if spectrum.outliers_limit is not None:
                inds = np.where(y0 > spectrum.outliers_limit)[0]
                if len(inds) > 0:
                    self.ax.plot(x0[inds], y0[inds], 'o', c='lime')

        if self.current_spectrum.outliers_limit is not None:
            self.ax.plot(x0, self.current_spectrum.outliers_limit, 'r-', lw=2)

        if self.figure_settings.params['x-log'].get() == 'On':
            self.ax.set_xscale("log")

        if self.figure_settings.params['y-log'].get() == 'On':
            self.ax.set_yscale("log")

        self.canvas.draw()

        def on_press(event):
            """ Highlight spectra close to the mouse click position """
            if self.lines is not None and event.inaxes == self.ax:
                fselector.lbox.selection_clear(0, END)
                # reassign standard properties to the previous nearest lines
                for line in self.nearest_lines:
                    line.set(linewidth=0.2, color='k', zorder=0)
                title = None
                self.nearest_lines, labels = [], []
                for i, line in enumerate(self.lines):
                    if line.contains(event)[0]:
                        fselector.select_item(i)
                        if len(self.nearest_lines) < 10:
                            color = CMAP(len(self.nearest_lines))
                            line.set(linewidth=1, color=color, zorder=1)
                            self.nearest_lines.append(line)
                            label = os.path.basename(fselector.filenames[i])
                            labels.append(label)
                        else:
                            title = "The nearest lines exceed 10.\n"
                            title += "  Show the first 10 ones"
                        # adapt the scrollbar cursor position to the first line
                        if len(self.nearest_lines) == 1:
                            cursor_position = i / len(fselector.filenames)
                            fselector.lbox.yview_moveto(cursor_position)
                            fselector.lbox.update()
                self.ax.legend(self.nearest_lines, labels, title=title, loc=1)
                self.canvas.draw()

        # disconnection to avoid show_all()/plot() mode mismatching
        for cid in self.cids:
            self.canvas.mpl_disconnect(cid)

        self.cids = [self.canvas.mpl_connect('button_press_event', on_press)]

    def show_hide_results(self, view):
        """ Show/Hide the 'paramsview' or the 'statsview' """
        if view == 'params':
            self.paramsview.show_hide()
        else:
            self.statsview.show_hide()
        # Make 'Frame Peaks' enable to see the changes in the plot
        self.selected_frame = 'Peaks'
        self.fr_fit.enable()
        self.fr_baseline.disable()

    def save_results(self, dirname_res=None):
        """ Save all results (peaks parameters) in .csv files """
        if dirname_res is None:
            dirname_res = fd.askdirectory(title='Select directory')
        else:
            if not os.path.exists(dirname_res):
                os.makedirs(dirname_res)

        if os.path.isdir(dirname_res):
            self.spectra.save_results(dirname_res, self.fileselector.filenames)

    def load_model(self, fname_json=None):
        """ Load a model from a .json file """
        if fname_json is None:
            fname_json = fd.askopenfilename(title='Select file',
                                            filetypes=[("json files", ".json")])
        if os.path.isfile(fname_json):
            self.model_dict = self.spectra.load_model(fname_json)

            self.text_model.delete(1.0, END)
            self.text_model.insert(1.0, os.path.basename(fname_json))

    def get_ncpus(self, nfiles):
        """ Return the number of CPUs to work with """
        ncpus = self.ncpus or self.fit_settings.params['ncpus'].get()
        if ncpus == "auto":
            return max(1, min(int(nfiles / 8), int(os.cpu_count() / 2)))
        else:
            return int(ncpus)

    def apply_model(self, model_dict=None, fnames=None, fit_params=None, ncpus=None):
        """ Apply model to the selected spectra """
        model_dict = model_dict or deepcopy(self.model_dict)

        if model_dict is None:
            showerror(message='No model has been loaded')
            return

        if fit_params is not None:
            model_dict['fit_params'] = fit_params

        if fnames is None:
            fnames = self.fileselector.filenames
            fnames = [fnames[i] for i in self.fileselector.lbox.curselection()]

        nfiles = len(fnames)
        ncpus = ncpus or self.get_ncpus(nfiles=nfiles)

        self.spectra.pbar_index = 0
        args = (model_dict, fnames, ncpus)
        thread = Thread(target=self.spectra.apply_model, args=args)
        thread.start()
        self.progressbar.update(self.spectra, nfiles, ncpus)
        thread.join()
        self.colorize_from_fit_status(fnames)
        self.reassign_current_spectrum(self.current_spectrum.fname)
        self.update()

    def apply_model_to_all(self):
        """ Apply model to the all the spectra """
        self.apply_model(fnames=self.spectra.fnames)

    def messagebox_continue(self, fnames):
        """ Open a messagebox if no models are found and return True/False
            concerning process continuation  """
        no_models = []
        for fname in fnames:
            for spectrum in self.spectra:
                if spectrum.fname == fname:
                    if len(spectrum.peak_models) == 0:
                        no_models.append(os.path.basename(fname))
                    break

        if len(no_models) > 0:
            msg = 'No models found in :\n'
            for name in no_models:
                msg += f'   . {name}\n'
            msg += 'Continue ?'.center(24)
            return askyesno('', msg)
        else:
            return True

    def save(self, fnames, fname_json=None):
        """ Save spectra in a .json file """

        if not self.messagebox_continue(fnames):
            return

        if fname_json is None:
            fname_json = fd.asksaveasfilename(defaultextension='.json')
            if fname_json == '':
                return

        if check_or_rename(fname_json) == fname_json:
            self.spectra.save(fname_json, fnames)
        else:
            msg = 'File {} is open. Close it or rename it'
            print(msg.format(os.path.basename(fname_json)))

    def save_selection(self, fname_json=None):
        """ Save selected spectra models in a .json file """
        inds = self.fileselector.lbox.curselection()
        if len(inds) == 0:
            showerror(message='No files have been selected')
            return
        fnames = [self.fileselector.filenames[i] for i in inds]
        self.save(fnames, fname_json=fname_json)

    def save_all(self, fname_json=None):
        """ Save all spectra models in a .json file """
        fnames = self.fileselector.filenames
        self.save(fnames, fname_json=fname_json)

    def reload(self, fname_json=None):
        """ Reload spectra models from a .json file """
        if fname_json is None:
            fname_json = fd.askopenfilename(title='Select file',
                                            filetypes=[("json files", ".json")])

        if os.path.isfile(fname_json):
            fselector = self.fileselector

            # remove previous loads
            fselector.lbox.delete(0, END)
            fselector.filenames = []

            for spectra_map in self.spectra.spectra_maps:
                spectra_map.frame.destroy()
                spectra_map.slider.disconnect(spectra_map.slider)

            self.spectra = Spectra.load(fname_json)

            for spectra_map in self.spectra.spectra_maps:
                self.frame_map_creation(spectra_map)
                spectra_map.plot_map(spectra_map.ax)

            for fname in self.spectra.fnames:
                fselector.lbox.insert(END, os.path.basename(fname))
                fselector.filenames.append(fname)
            fselector.lbox.select_set(0)
            self.update()

    def plot(self):
        """ Plot baseline and peak models after 'ax' clearing """
        if not self.show_plot or self.current_spectrum is None:
            return

        self.is_show_all = False

        if self.lines is not None:
            for line in self.lines:
                line.remove()
            self.lines = None

        # both baseline and spectrum are plotted together to adapt
        # the axis scale simultaneously with ax.clear()
        xlim, ylim = self.ax.get_xlim(), self.ax.get_ylim()

        self.ax.clear()

        # reassign previous axis limits (related to zoom)
        if self.preserve_axis.get() and not xlim == ylim == (0.0, 1.0):
            self.ax.set_xlim(xlim)
            self.ax.set_ylim(ylim)

        spectrum = self.current_spectrum
        fig_settings = self.figure_settings.params
        result_fit = spectrum.result_fit

        title = fig_settings['title'].get()
        if title == 'DEFAULT':
            title = os.path.basename(spectrum.fname)

        self.ax.set_title(title, fontsize=18, zorder=-1)
        self.ax.set_xlabel(fig_settings['x_label'].get(), fontsize=18)
        self.ax.set_ylabel(fig_settings['y_label'].get(), fontsize=18)

        show_interactive_bounds = fig_settings['interactive_bounds'].get() == 'On'
        if fig_settings['plot_fit'].get() == 'On':
            show_weights = fig_settings['plot_weights'].get() == 'On'
            show_outliers = fig_settings['plot_outliers'].get() == 'On'
            show_outl_limit = fig_settings['plot_outliers_limit'].get() == 'On'
            show_neg_values = fig_settings['plot_negative_values'].get() == 'On'
            show_noise_level = fig_settings['plot_noise_level'].get() == 'On'
            show_baseline = fig_settings['plot_baseline'].get() == 'On'
            show_background = fig_settings['plot_background'].get() == 'On'
            subtract_baseline = subtract_bkg = self.subtract_baseline_bkg.get()
            self.lines = spectrum.plot(self.ax,
                                       show_weights=show_weights,
                                       show_outliers=show_outliers,
                                       show_outliers_limit=show_outl_limit,
                                       show_negative_values=show_neg_values,
                                       show_noise_level=show_noise_level,
                                       show_peak_models=show_interactive_bounds,
                                       show_baseline=show_baseline,
                                       show_background=show_background,
                                       subtract_baseline=subtract_baseline,
                                       subtract_bkg=subtract_bkg)
            line_bkg_visible = show_background and spectrum.bkg_model

            # baseline plotting
            baseline = spectrum.baseline
            if not baseline.is_subtracted:
                x, y = spectrum.x, None
                if baseline.attached or baseline.mode == 'Semi-Auto':
                    y = spectrum.y
                baseline.plot(self.ax, x, y, attached=baseline.attached)

            if show_interactive_bounds:
                self.ibounds.update()

            self.ax.legend()
            self.tmp = None
            linewidth = 0.5
            if hasattr(result_fit, "success") and result_fit.success:
                linewidth = 1

            def annotate_params(i, color='k'):
                """ Annotate figure with fit parameters """
                if not line_bkg_visible:
                    model = spectrum.peak_models[i]
                    x0 = model.param_hints['x0']['value']
                elif i == 0:
                    model = spectrum.bkg_model
                    x0 = 0.5 * (x[0] + x[-1])
                else:
                    model = spectrum.peak_models[i - 1]
                    x0 = model.param_hints['x0']['value']

                y0 = model.eval(model.make_params(), x=x0)
                xy = (x0, min(y0, self.ax.get_ylim()[1]))

                text = []
                for key in ['x0', 'ampli', 'fwhm', 'fwhm_l', 'fwhm_r']:
                    if key in model.param_hints:
                        text.append(f"{key}: {model.param_hints[key]['value']:.4g}")
                text = '\n'.join(text)

                bbox = dict(facecolor='w', edgecolor=color, boxstyle='round')
                self.tmp = self.ax.annotate(text, xy=xy, xycoords='data',
                                            bbox=bbox, verticalalignment='top')

            def on_motion(event):
                """ Highlight model when hovering with the mouse """
                if event.inaxes == self.ax and self.lines is not None and len(self.lines) > 1:
                    for i, line in enumerate(self.lines[1:]):
                        if line.contains(event)[0]:
                            line.set_linewidth(3)
                            if self.tmp is not None:
                                self.tmp.remove()
                            annotate_params(i, color=line.get_c())
                        else:
                            line.set_linewidth(linewidth)
                    self.canvas.draw_idle()

        if fig_settings['plot_outliers_limit'].get() == 'On':
            if spectrum.outliers_limit is not None:
                x, x0 = spectrum.x, list(spectrum.x0)
                imin, imax = x0.index(x[0]), x0.index(x[-1])
                y_outliers_limit = spectrum.outliers_limit[imin:imax + 1]
                self.ax.plot(x, y_outliers_limit, 'r', label="Outliers limit")
                self.ax.legend()

        if fig_settings['plot_residual'].get() == 'On':
            coef_residual = fig_settings['coef_residual'].get()
            spectrum.plot_residual(self.ax, factor=coef_residual)

        if fig_settings['show_peaks_labels'].get() == 'On':
            dy = 0.02 * spectrum.y.max()
            for i, label in enumerate(spectrum.peak_labels):
                if label == '':
                    continue
                model = spectrum.peak_models[i]
                x0 = model.param_hints['x0']['value']
                y = spectrum.y[closest_index(spectrum.x, x0)]
                xy = (x0, y + dy)
                xytext = (x0, y + 4 * dy)
                self.ax.annotate(label, xy=xy, xytext=xytext, xycoords='data',
                                 ha='center', size=14, arrowprops=dict(fc='k'))

        def on_press(event):
            """ Callback function associated to the mouse press event """

            # Do not add baseline or peak points when pan or zoom are selected
            toolbar_buttons = self.canvas.toolbar._buttons
            if toolbar_buttons['Pan'].var.get() or \
                    toolbar_buttons['Zoom'].var.get():
                return

            if event.inaxes == self.ax and spectrum is not None:
                x, y = event.xdata, event.ydata
                action = 'add' if event.button == 1 else 'del'
                # frame = self.selected_frame.get()
                frame = self.selected_frame
                if frame == 'Baseline':
                    eval(f"self.{action}_baseline_point")(x, y)
                elif frame == 'Fitting':
                    if not self.ibounds.interact_with_bbox(event):
                        eval(f"self.{action}_peaks_point")(x, y)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.ax.get_figure().tight_layout()
        self.canvas.draw()

        # disconnection and to avoid show_all()/plot() mode mismatching
        for cid in self.cids:
            self.canvas.mpl_disconnect(cid)

        self.cids = [self.canvas.mpl_connect('motion_notify_event', on_motion),
                     self.canvas.mpl_connect('button_press_event', on_press)]

    def on_press_baseline_peaks(self, event):
        """ Callback function associated to the mouse press event in
            the 'Baseline' and 'Peaks' LabelFrames for enabling/disabling """
        frame = event.widget.config()['text'][-1]
        if frame == "Baseline":
            self.fr_fit.disable()
            if self.selected_frame != "Baseline":
                self.fr_baseline.enable()
                self.selected_frame = "Baseline"
            else:
                self.fr_baseline.disable()
                self.selected_frame = None
        elif frame == "Fitting":
            self.fr_baseline.disable()
            if self.selected_frame != "Fitting":
                self.fr_fit.enable()
                self.selected_frame = "Fitting"
            else:
                self.fr_fit.disable()
                self.selected_frame = None

    def baseline_is_subtracted_message(self):
        """ Show an error message associated with the baseline """
        msg = "This action will reinitialize the spectrum.\n"
        msg += 'Continue ?'
        return askyesno(message=msg)

    def add_baseline_point(self, x, y):
        """ Add baseline point from the (x,y)-coordinate """
        if self.current_spectrum.baseline.mode not in ['Linear', 'Polynomial']:
            return

        if self.current_spectrum.baseline.is_subtracted:
            if not self.baseline_is_subtracted_message():
                return
            self.current_spectrum.load_profile(self.current_spectrum.fname)
            self.current_spectrum.apply_range()
            self.current_spectrum.baseline.is_subtracted = False
            self.current_spectrum.baseline.points = [[], []]

        self.current_spectrum.baseline.add_point(x, y)

        plot_baseline = self.figure_settings.params['plot_baseline'].get()
        self.figure_settings.params['plot_baseline'].set('off')
        self.plot()
        self.figure_settings.params['plot_baseline'].set(plot_baseline)

    def del_baseline_point(self, x, _):
        """ Delete the closest baseline 'x'-point """
        if len(self.current_spectrum.baseline.points[0]) == 0:
            return
        dist_min = np.inf
        for i, x0 in enumerate(self.current_spectrum.baseline.points[0]):
            dist = abs(x0 - x)
            if dist < dist_min:
                dist_min, ind_min = dist, i
        self.current_spectrum.baseline.points[0].pop(ind_min)
        self.current_spectrum.baseline.points[1].pop(ind_min)
        self.plot()

    def apply_baseline_settings(self, fnames=None):
        """ Apply baseline settings """

        keys = ['mode', 'coef', 'order_max', 'sigma', 'attached']
        for key in keys:
            val = eval(f"self.baseline_{key}").get()
            setattr(self.current_spectrum.baseline, key, val)

        if fnames is None:
            fnames = self.fileselector.filenames
            fnames = [fnames[i] for i in self.fileselector.lbox.curselection()]

        for fname in fnames:
            spectrum, _ = self.spectra.get_objects(fname)
            spectrum.result_fit = lambda: None
            for key, value in vars(self.current_spectrum.baseline).items():
                setattr(spectrum.baseline, key, value)
        self.colorize_from_fit_status(fnames)  # reassign white

        self.current_spectrum.preprocess()
        self.paramsview.delete()
        self.statsview.delete()
        self.plot()

    def apply_baseline_settings_to_all(self):
        """ Apply baseline settings to all the spectra """
        self.apply_baseline_settings(fnames=self.spectra.fnames)

    def set_baseline_settings(self):
        """ Set baseline settings from the baseline to the appli """
        for x in ['mode', 'coef', 'order_max', 'sigma', 'attached']:
            eval(f'self.baseline_{x}.set(self.current_spectrum.baseline.{x})')

    def load_baseline(self, fname=None):
        """ Load a baseline from a row-column .txt file """
        if self.current_spectrum.baseline.is_subtracted:
            if not self.baseline_is_subtracted_message():
                return

        if fname is None:
            fname = fd.askopenfilename(title='Select file')

        if os.path.isfile(fname):
            self.current_spectrum.baseline.load_baseline(fname)
            self.plot()

    def load_user_model(self, model):
        """Load users model from file to be added to PEAK_MODELS or BKG_MODEL"""
        fname = fd.askopenfilename(title='Select file',
                                   filetypes=[("", "*.txt;*.py")])
        if fname is not None:
            if Path(fname).suffix == '.txt':
                load_models_from_txt(fname, eval(f"{model}"))
            else:
                load_models_from_py(fname)

    def add_peaks_point(self, x, y):
        """ Add peak from the (x,y)-coordinates """

        # to take into account the strong aspect ratio in the axis represent.
        ratio = 1. / self.ax.get_data_ratio() ** 2

        inds = range(len(self.current_spectrum.x))

        x_sp, y_sp = self.current_spectrum.x, self.current_spectrum.y
        dist_min = np.inf
        for ind in inds:
            dist = (x_sp[ind] - x) ** 2 + ratio * (y_sp[ind] - y) ** 2
            if dist < dist_min:
                dist_min, ind_min = dist, ind

        model_name = self.model.get()
        self.current_spectrum.add_peak_model(model_name, x0=x_sp[ind_min])
        self.current_spectrum.result_fit = lambda: None

        self.paramsview.update()
        self.plot()

    def del_peaks_point(self, x, _):
        """ Delete the closest peak 'x'-point """
        if len(self.current_spectrum.peak_models) > 0:
            dist_min = np.inf
            for i, peak_model in enumerate(self.current_spectrum.peak_models):
                x0 = peak_model.param_hints["x0"]["value"]
                dist = abs(x0 - x)
                if dist < dist_min:
                    dist_min, ind_min = dist, i
            self.current_spectrum.del_peak_model(ind_min)
            self.current_spectrum.result_fit = lambda: None

        self.paramsview.update()
        self.plot()

    def auto_peaks(self, model_name=None):
        """ Define peaks from automatic detection """
        if model_name is None:
            model_name = self.model.get()
        self.current_spectrum.auto_peaks(model_name)
        self.paramsview.update()
        self.statsview.update()
        self.plot()

    def set_bkg_model(self):
        """ Set bkg_model """
        if self.current_spectrum is not None:
            self.current_spectrum.set_bkg_model(self.bkg_name.get())
            self.current_spectrum.result_fit = lambda: None
            self.paramsview.update()
            self.plot()

    def update_fit_settings(self):
        """ Update fit settings """
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        self.fit_settings.update(x, y)

    def colorize_from_fit_status(self, fnames):
        """ Colorize the fileselector items from the fit success status """
        for fname in fnames:
            ind_fselector = self.fileselector.filenames.index(fname)
            spectrum, _ = self.spectra.get_objects(fname)
            result_fit = spectrum.result_fit
            if hasattr(result_fit, 'success'):
                color = 'Lime' if result_fit.success else 'Orange'
            else:
                color = 'white'
            self.fileselector.lbox.itemconfig(ind_fselector, {'bg': color})

    def fit(self, fnames=None):
        """ Fit the peaks """
        params = self.fit_settings.params
        fit_params = {}
        fit_params['fit_negative'] = params['fit_negative_values'].get() == 'On'
        fit_params['fit_outliers'] = params['fit_outliers'].get() == 'On'
        fit_params['independent_models'] = params['independent_models'].get() == 'On'
        fit_params['coef_noise'] = params['coef_noise'].get()
        fit_params['max_ite'] = params['maximum_iterations'].get()
        fit_params['method'] = params['method'].get()
        fit_params['xtol'] = params['xtol'].get()

        model_dict = self.current_spectrum.save()

        self.apply_model(model_dict=model_dict, fnames=fnames,
                         fit_params=fit_params)

    def fit_all(self):
        """ Fit the peaks for all the spectra """
        self.fit(fnames=self.spectra.fnames)

    def set_range(self):
        """ Set range from the spectrum to the appli """
        self.range_min.set(self.current_spectrum.range_min)
        self.range_max.set(self.current_spectrum.range_max)

    def apply_range(self, fnames=None):
        """ Set an apply range to the spectrum/spectra """

        range_min = self.get_value('range_min')
        range_max = self.get_value('range_max')

        if range_min is not None and range_max is not None:
            if range_min >= range_max:
                showerror(message="incorrect values: range_min >= range_max)")
                self.set_range()
                return

        if fnames is None:
            fnames = self.fileselector.filenames
            fnames = [fnames[i] for i in self.fileselector.lbox.curselection()]

        for fname in fnames:
            spectrum, _ = self.spectra.get_objects(fname)
            spectrum.result_fit = lambda: None
            spectrum.range_min = range_min
            spectrum.range_max = range_max
        self.colorize_from_fit_status(fnames)  # reassign white

        self.current_spectrum.preprocess()
        self.set_range()
        self.paramsview.delete()
        self.statsview.delete()
        self.plot()

    def apply_range_to_all(self):
        """ Set and apply range to all the spectra """
        self.apply_range(fnames=self.spectra.fnames)

    def update_normalize(self):
        """ Update 'normalize' to all the spectra """

        normalize = self.normalize.get()

        for spectrum in self.spectra.all:
            spectrum.result_fit = lambda: None
            spectrum.normalize = normalize
        self.colorize_from_fit_status(self.spectra.fnames)  # reassign white

        self.current_spectrum.preprocess()
        self.paramsview.delete()
        self.statsview.delete()
        self.plot()

    def get_value(self, name):
        """ Return the float value related to the 'name' attribute """
        try:
            return float(eval(f"self.{name}.get()"))
        except:
            return None

    def update_normalize_range(self):
        """ Update the normalization ranges to all the spectra """

        normalize_range_min = self.get_value('normalize_range_min')
        normalize_range_max = self.get_value('normalize_range_max')

        if normalize_range_min is not None and normalize_range_max is not None:
            if normalize_range_min >= normalize_range_max:
                showerror(message="incorrect values: range_min >= range_max)")
                self.set_normalize_settings()
                return

        for spectrum in self.spectra.all:
            spectrum.result_fit = lambda: None
            spectrum.normalize_range_min = normalize_range_min
            spectrum.normalize_range_max = normalize_range_max
        self.colorize_from_fit_status(self.spectra.fnames)  # reassign white

        self.current_spectrum.preprocess()
        self.paramsview.delete()
        self.statsview.delete()
        self.plot()

    def set_normalize_settings(self):
        """ Set normalize settings from the spectrum to the appli """
        self.normalize.set(self.current_spectrum.normalize)
        self.normalize_range_min.set(self.current_spectrum.normalize_range_min)
        self.normalize_range_max.set(self.current_spectrum.normalize_range_max)

    def reinit(self, fnames=None):
        """ Reinitialize the spectrum """
        if fnames is None:
            fnames = self.fileselector.filenames
            fnames = [fnames[i] for i in self.fileselector.lbox.curselection()]

        for fname in fnames:
            spectrum, _ = self.spectra.get_objects(fname)
            spectrum.reinit()

        self.colorize_from_fit_status(fnames)  # reassign white
        self.paramsview.delete()
        self.statsview.delete()
        self.set_range()
        self.set_baseline_settings()
        self.set_normalize_settings()
        self.bkg_name.set('None')
        self.plot()

    def reinit_all(self):
        """ Reinitialize all the spectra """
        self.reinit(fnames=self.spectra.fnames)

    def reassign_current_spectrum(self, fname):
        """ Reassign the current spectrum from 'fname' """
        ind = self.fileselector.filenames.index(fname)
        self.fileselector.select_item(ind)
        self.current_spectrum, _ = self.spectra.get_objects(fname)
        self.set_range()
        self.set_baseline_settings()
        self.plot()

    def remove(self, delete_tabview=True):
        """ Remove all the features (spectrum attributes, baseline, tabview) """
        if self.current_spectrum is not None:
            self.current_spectrum.remove_models()
            self.current_spectrum.baseline.points = [[], []]

            if delete_tabview:  # expensive operation when doing a lot of times
                self.paramsview.delete()
                self.statsview.delete()
            self.plot()

    def auto_eval(self, model_name=None, fnames=None):
        """ Fit spectrum after evaluating baseline and peaks automatically """
        if fnames is None:
            fnames = self.fileselector.filenames
            fnames = [fnames[i] for i in self.fileselector.lbox.curselection()]

        self.show_plot = False
        current_fname = self.current_spectrum.fname
        for fname in fnames:
            self.current_spectrum, _ = self.spectra.get_objects(fname)
            self.current_spectrum.apply_range()
            self.current_spectrum.baseline.mode = 'Semi-Auto'
            self.current_spectrum.eval_baseline()
            self.current_spectrum.subtract_baseline()
            self.auto_peaks(model_name=model_name)
        self.colorize_from_fit_status(fnames)
        self.show_plot = True
        self.reassign_current_spectrum(current_fname)

    def auto_eval_all(self, model_name=None):
        """ Apply automatic fitting on all spectra  """
        self.auto_eval(model_name=model_name, fnames=self.spectra.fnames)

    def delete_all(self, _):
        """ Delete all spectra """
        self.ax.clear()
        self.canvas.draw()
        for spectra_map in self.spectra.spectra_maps:
            spectra_map.frame.destroy()
            spectra_map.slider.disconnect(spectra_map.slider)
        self.spectra = Spectra()

    def delete(self, fnames=None):
        """ Delete items from spectra selected in the 'fileselector'
            or passed as argument """
        fselector = self.fileselector
        fnames_fselector = fselector.filenames

        if isinstance(fnames, list):
            for fname in fnames:
                if fname in fnames_fselector:
                    ind = fnames_fselector.index(fname)
                    self.fileselector.lbox.delete(ind)
                    self.fileselector.filenames.pop(ind)

        fnames_fselector = fselector.filenames
        for fname_spectra in self.spectra.fnames:
            if fname_spectra not in fnames_fselector:
                spectrum, spectra = self.spectra.get_objects(fname_spectra)
                if isinstance(spectra, SpectraMap):
                    spectra.arr[spectra.index(spectrum)] = np.nan
                spectra.remove(spectrum)

        for spectra in self.spectra.spectra_maps:
            spectra.plot_map_update()

        if len(fselector.lbox.curselection()) == 0:
            self.remove()
            self.ax.clear()
            self.canvas.draw()

    def add_items_from_dir(self, dirname):
        """ Add new items related to a  'dirname' """
        if not os.path.isdir(dirname):
            print(f"{dirname} is not an existing directory")
        else:
            fnames = glob.glob(os.path.join(dirname, '*.txt'))
            self.add_items(fnames)

    def add_items(self, fnames=None):
        """ Add new items from a 'fnames' list """
        if isinstance(fnames, list):
            for fname in fnames:
                if fname not in self.fileselector.filenames:
                    self.fileselector.add_items(filenames=[fname])

        # create Spectrum or SpectramMap objects associated to the new items
        fname_first_item = None
        fnames = self.spectra.fnames
        for fname in self.fileselector.filenames:
            if fname not in fnames:

                dim = get_dim(fname)

                if dim is None:
                    msg = "The file {} can not be interpreted by fitspy"
                    showerror(message=msg.format(Path(fname).name))
                    return

                elif dim == 2:
                    self.create_map(fname)
                    return

                else:  # dim == 1
                    try:
                        spectrum = Spectrum()
                        spectrum.fname = fname

                        spectrum.preprocess()
                        self.spectra.append(spectrum)

                        if fname_first_item is None:
                            fname_first_item = fname
                    except:
                        pass

        if fname_first_item is not None:
            self.update(fname=fname_first_item)

    def update_markers(self, fname):
        """  Markers management in 2D-maps """

        # remove all markers
        for spectra_map in self.spectra.spectra_maps:
            if spectra_map.marker is not None:
                [x.remove() for x in spectra_map.marker]
            spectra_map.canvas.draw()
            spectra_map.marker = None

        # set marker in the appropriate 2D-map
        spectrum, spectra_map = self.spectra.get_objects(fname)
        ax = spectra_map.ax
        ind = spectra_map.index(spectrum)
        x, y = spectra_map.coords[ind]
        spectra_map.marker = ax.plot(x, y, 'rs', ms=9, mfc='none')
        ax.set_xlim(spectra_map.extent[0], spectra_map.extent[1])
        ax.set_ylim(spectra_map.extent[2], spectra_map.extent[3])
        spectra_map.canvas.draw()

    def update(self, fname=None):
        """ Update the appli with the spectrum selected in the 'fileselector'
            or passed as argument """

        if isinstance(fname, str):
            if fname not in self.fileselector.filenames:
                self.fileselector.add_items(filenames=[fname])
            ind = self.fileselector.filenames.index(fname)
            self.fileselector.select_item(ind)

        else:
            # get fname from the first cursor selection
            ind = self.fileselector.lbox.curselection()[0]
            fname = self.fileselector.filenames[ind]
            self.fileselector.select_item(ind, selection_clear=False)

        if "X=" in fname:
            self.update_markers(fname)

        self.current_spectrum, _ = self.spectra.get_objects(fname)
        self.current_spectrum.preprocess()
        self.ibounds = InteractiveBounds(self.current_spectrum, self.ax, bind_func=self.refresh)

        self.show_plot = False
        self.set_range()
        self.set_baseline_settings()
        self.set_normalize_settings()
        self.paramsview.spectrum = self.current_spectrum
        self.paramsview.bkg_name = self.bkg_name
        self.paramsview.plot = self.plot
        self.paramsview.update()
        self.statsview.spectrum = self.current_spectrum
        self.statsview.update()
        self.show_plot = True
        self.plot()

    def refresh(self):
        self.paramsview.params_has_changed()
        self.plot()

    def create_map(self, fname):
        """ Create the 2D-map that consists in replacing the current spectra by
            the ones issued from the 2D-map extrusion """

        spectra_map = SpectraMap()
        spectra_map.create_map(fname)
        self.spectra.spectra_maps.append(spectra_map)
        self.frame_map_creation(spectra_map)
        spectra_map.plot_map(spectra_map.ax)

        # remove 2D-map filename in the fileselector
        ind = self.fileselector.filenames.index(fname)
        self.fileselector.lbox.delete(ind)
        self.fileselector.filenames.pop(ind)

        # add each spectra related to the 2D-map
        fnames = [spectrum.fname for spectrum in spectra_map]
        self.add_items(fnames=fnames)

        # force cursor location at the first item
        self.update(fnames[0])
