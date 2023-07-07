"""
Callback functions encapsulated in a class to interact with the GUI
"""
import os
from tkinter import END
from tkinter.messagebox import askyesno, showerror
from tkinter import filedialog as fd
from copy import deepcopy
import glob
import numpy as np
import matplotlib.pyplot as plt

from fitspy.spectra import Spectrum, Spectra, SpectraMap, fit_mp
from fitspy.utils import closest_index, check_or_rename

FIT_METHODS = {'Leastsq': 'leastsq', 'Least_squares': 'least_squares',
               'Nelder-Mead': 'nelder', 'SLSQP': 'slsqp'}
CMAP = plt.get_cmap("tab10")


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
        self.lines = None
        self.nearest_lines = []
        self.tmp = None
        self.selected_frame = "Baseline"
        self.model_dict = None
        self.ncpus = None

    def update_figure_settings(self):
        """ Update attractors settings """
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        self.figure_settings.update(x, y, bind_fun=self.plot)

    def rescale(self):
        """ Rescale the figure """
        self.ax.autoscale()
        self.canvas.draw()
        self.canvas.toolbar.update()

    def show_all(self):
        """ Show all spectra and highlight spectrum on mouse over """
        fselector = self.fileselector

        xlim, ylim = self.ax.get_xlim(), self.ax.get_ylim()
        self.ax.clear()

        # reassign previous axis limits (related to zoom)
        if not xlim == ylim == (0.0, 1.0):
            self.ax.set_xlim(xlim)
            self.ax.set_ylim(ylim)

        self.lines = []
        for fname in fselector.filenames[0]:
            spectrum, _ = self.spectra.get_objects(fname)
            x, y = spectrum.x0, spectrum.y0
            self.lines.append(self.ax.plot(x, y, 'k-', lw=0.2, zorder=0)[0])
        self.canvas.draw()

        def on_press(event):
            """ Highlight spectra close to the mouse click position """
            if self.lines is not None and event.inaxes == self.ax:
                fselector.lbox[0].selection_clear(0, END)
                # reassign standard properties to the previous nearest lines
                for line in self.nearest_lines:
                    line.set(linewidth=0.2, color='k', zorder=0)
                title = None
                self.nearest_lines, labels = [], []
                for i, line in enumerate(self.lines):
                    if line.contains(event)[0]:
                        fselector.lbox[0].selection_set(i)
                        if len(self.nearest_lines) < 10:
                            color = CMAP(len(self.nearest_lines))
                            line.set(linewidth=1, color=color, zorder=1)
                            self.nearest_lines.append(line)
                            label = os.path.basename(fselector.filenames[0][i])
                            labels.append(label)
                        else:
                            title = "The nearest lines exceed 10.\n"
                            title += "  Show the first 10 ones"
                        # adapt the scrollbar cursor position to the first line
                        if len(self.nearest_lines) == 1:
                            cursor_position = i / len(fselector.filenames[0])
                            fselector.lbox[0].yview_moveto(cursor_position)
                            fselector.lbox[0].update()
                self.ax.legend(self.nearest_lines, labels, title=title, loc=1)
                self.canvas.draw()

        # disconnection to avoid show_all()/plot() mode mismatching
        for cid in self.cids:
            self.canvas.mpl_disconnect(cid)

        self.cids = [self.canvas.mpl_connect('button_press_event', on_press)]

    def show_hide_results(self):
        """ Show/Hide the results 'tabview' """
        self.tabview.show_hide()
        # Make 'Frame Peaks' enable to see the changes in the plot
        self.selected_frame = 'Peaks'
        self.fr_peaks.enable()
        self.fr_baseline.disable()

    def save_results(self, dirname_res=None):
        """ Save all spectra (peaks) results in .csv files """
        if dirname_res is None:
            dirname_res = fd.askdirectory(title='Select directory')
        else:
            if not os.path.exists(dirname_res):
                os.makedirs(dirname_res)

        if os.path.isdir(dirname_res):
            self.spectra.save_results(dirname_res,
                                      self.fileselector.filenames[0])

    def save_figures(self, dirname_fig=None):
        """ Save all spectra figures in .png files """
        if dirname_fig is None:
            dirname_fig = fd.askdirectory(title='Select directory')
        else:
            if not os.path.exists(dirname_fig):
                os.makedirs(dirname_fig)

        if os.path.isdir(dirname_fig):
            bounds = (self.ax.get_xlim(), self.ax.get_ylim())
            self.spectra.save_figures(dirname_fig,
                                      fnames=self.fileselector.filenames[0],
                                      bounds=bounds)

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
            return max(1, min(int(nfiles / 4), int(os.cpu_count() / 2)))
        else:
            return int(ncpus)

    def apply_model(self, fnames=None, selection=False):
        """ Apply model to the selected spectra """
        fselector = self.fileselector

        if self.model_dict is None:
            showerror(message='No model has been loaded')
            return

        if fnames is None:
            fnames = fselector.filenames[0]

        if selection:
            fnames = fselector.filenames[0]
            fnames = [fnames[i] for i in fselector.lbox[0].curselection()]

        params = self.fit_settings.params
        kwargs = {'fit_negative': params['fit_negative_values'].get() == 'On',
                  'max_ite': params['maximum_iterations'].get(),
                  'fit_method': params['fit_method'].get()}

        ncpus = self.get_ncpus(nfiles=len(fnames))
        self.spectra.apply_model(self.model_dict, fnames, ncpus, **kwargs)
        self.colorize_from_fit_status(fnames)
        self.update()

    def messagebox_continue(self, fnames):
        """ Open a messagebox if no models are found and return True/False
            concerning process continuation  """
        no_models = []
        for fname in fnames:
            for spectrum in self.spectra:
                if spectrum.fname == fname:
                    if len(spectrum.models) == 0:
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
        inds = self.fileselector.lbox[0].curselection()
        if len(inds) == 0:
            showerror(message='No files have been selected')
            return
        fnames = [self.fileselector.filenames[0][i] for i in inds]
        self.save(fnames, fname_json=fname_json)

    def save_all(self, fname_json=None):
        """ Save all spectra models in a .json file """
        fnames = self.fileselector.filenames[0]
        self.save(fnames, fname_json=fname_json)

    def reload(self, fname_json=None):
        """ Reload spectra models from a .json file """
        if fname_json is None:
            fname_json = fd.askopenfilename(title='Select file',
                                            filetypes=[("json files", ".json")])

        if os.path.isfile(fname_json):
            fselector = self.fileselector

            # remove previous loads
            fselector.lbox[0].delete(0, END)
            fselector.filenames[0] = []

            self.spectra = Spectra.load(fname_json)

            for spectra_map in self.spectra.spectra_maps:
                self.frame_map_creation(spectra_map)
                spectra_map.plot_map(spectra_map.ax)

            for fname in self.spectra.fnames:
                fselector.lbox[0].insert(END, os.path.basename(fname))
                fselector.filenames[0].append(fname)
            fselector.lbox[0].select_set(0)
            self.update()

    def plot(self):
        """ Plot baseline and spectrum models after 'ax' clearing """
        if not self.show_plot or self.current_spectrum is None:
            return

        if self.lines is not None:
            for line in self.lines:
                line.remove()
            self.lines = None

        # both baseline and spectrum are plotted together to adapt
        # the axis scale simultaneously with ax.clear()
        xlim, ylim = self.ax.get_xlim(), self.ax.get_ylim()
        self.ax.clear()

        # reassign previous axis limits (related to zoom)
        if not xlim == ylim == (0.0, 1.0):
            self.ax.set_xlim(xlim)
            self.ax.set_ylim(ylim)

        spectrum = self.current_spectrum
        fig_settings = self.figure_settings.params

        title = fig_settings['title'].get()
        if title == 'DEFAULT':
            title = os.path.basename(spectrum.fname)

        self.ax.set_title(title, fontsize=18, zorder=-1)
        self.ax.set_xlabel(fig_settings['x_label'].get(), fontsize=18)
        self.ax.set_ylabel(fig_settings['y_label'].get(), fontsize=18)

        if fig_settings['plot_fit'].get() == 'On':
            show_peaks = self.attractors.get()
            show_neg_values = fig_settings['plot_negative_values'].get() == 'On'
            self.lines = spectrum.plot(self.ax,
                                       show_peaks=show_peaks,
                                       show_negative_values=show_neg_values)

            # baseline parameters updating
            spectrum.baseline.mode = self.baseline_mode.get()
            spectrum.baseline.order_max = self.baseline_order_max.get()

            # baseline plotting
            x = spectrum.x
            y = spectrum.y if self.attached.get() else None
            spectrum.baseline.plot(self.ax, x=x, y=y, sigma=self.sigma.get())

            self.ax.legend()
            self.tmp = None

            def annotate_params(i, color='k'):
                """ Annotate figure with fit parameters """
                model = spectrum.models[i]
                x0 = model.param_hints['x0']['value']
                y0 = model.eval(model.make_params(), x=x0, der=0)
                xy = (x0, min(y0, self.ax.get_ylim()[1]))

                names = model.param_names
                text = ""
                for name in names:
                    param = spectrum.result_fit.params[name]
                    text += f"{name[4:]}: {param.value:.4g}"
                    if param.stderr is not None:
                        text += f" +/-{param.stderr:.2g}"
                    if name != names[-1]:
                        text += "\n"
                bbox = dict(facecolor='w', edgecolor=color, boxstyle='round')
                self.tmp = self.ax.annotate(text, xy=xy, xycoords='data',
                                            bbox=bbox, verticalalignment='top')

            def on_motion(event):
                """ Highlight model when hovering with the mouse """
                if self.lines is not None and event.inaxes == self.ax:
                    for i, line in enumerate(self.lines):
                        if line.contains(event)[0]:
                            line.set_linewidth(3)
                            if self.tmp is not None:
                                self.tmp.remove()
                            if spectrum.result_fit is not None:
                                annotate_params(i, color=line.get_c())
                        else:
                            line.set_linewidth(1)
                    self.canvas.draw_idle()

        if fig_settings['plot_residual'].get() == 'On':
            coef_residual = fig_settings['coef_residual'].get()
            spectrum.plot_residual(self.ax, factor=coef_residual)

        if fig_settings['show_peaks_labels'].get() == 'On':
            dy = 0.02 * spectrum.y.max()
            for i, label in enumerate(spectrum.models_labels):
                if label == '':
                    continue
                model = spectrum.models[i]
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
                if frame in ['Baseline', 'Peaks']:
                    eval(f"self.{action}_{frame.lower()}_point")(x, y)

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
            self.fr_peaks.disable()
            if self.selected_frame != "Baseline":
                self.fr_baseline.enable()
                self.selected_frame = "Baseline"
            else:
                self.fr_baseline.disable()
                self.selected_frame = None
        elif frame == "Peaks":
            self.fr_baseline.disable()
            if self.selected_frame != "Peaks":
                self.fr_peaks.enable()
                self.selected_frame = "Peaks"
            else:
                self.fr_peaks.disable()
                self.selected_frame = None

    def add_baseline_point(self, x, y):
        """ Add baseline point from the (x,y)-coordinate """
        self.current_spectrum.baseline.add_point(x, y)
        self.plot()

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

    def load_baseline(self, fname=None):
        """ Load a baseline from a row-column .txt file """
        if fname is None:
            fname = fd.askopenfilename(title='Select file')

        if os.path.isfile(fname):
            self.current_spectrum.baseline.load_baseline(fname)
            self.plot()

    def auto_baseline(self):
        """ Define baseline from automatic points selection """
        self.current_spectrum.baseline.distance = self.distance.get()
        self.current_spectrum.auto_baseline()
        self.plot()

    def substract_baseline(self, fnames=None):
        """ Substract the current baseline """
        baseline_points = self.current_spectrum.baseline.points
        if len(baseline_points[0]) == 0:
            return

        if fnames is None:
            fselector = self.fileselector
            fnames = fselector.filenames[0]
            fnames = [fnames[i] for i in fselector.lbox[0].curselection()]

        attached = self.attached.get()
        sigma = self.sigma.get()

        for fname in fnames:
            spectrum, _ = self.spectra.get_objects(fname)
            spectrum.baseline.points = baseline_points.copy()
            spectrum.substract_baseline(attached=attached, sigma=sigma)
            spectrum.baseline.points = [[], []]
        self.tabview.delete()
        self.ax.clear()
        self.plot()

    def substract_baseline_to_all(self):
        """ Substract baseline to all the spectra """
        self.substract_baseline(fnames=self.spectra.fnames)

    def delete_baseline(self):
        """ Delete the current baseline """
        self.current_spectrum.baseline.points = [[], []]
        self.plot()

    def update_attractors(self):
        """ Update attractors """
        if self.attractors.get():
            self.current_spectrum.peaks_calculation()
        self.plot()

    def update_attractors_settings(self):
        """ Update attractors settings """
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        self.attractors_settings.update(x, y, bind_fun=self.update_peaks)

    def update_peaks(self):
        """ Update peaks """
        self.current_spectrum.peaks_params = self.attractors_settings.params
        self.current_spectrum.peaks_calculation()
        self.plot()

    def add_peaks_point(self, x, y):
        """ Add peak (spectrum model) from the (x,y)-coordinates """

        # to take into account the strong aspect ratio in the axis represent.
        ratio = 1. / self.ax.get_data_ratio() ** 2

        if self.attractors.get():
            inds = self.current_spectrum.peaks
        else:
            inds = range(len(self.current_spectrum.x))

        x_sp, y_sp = self.current_spectrum.x, self.current_spectrum.y
        dist_min = np.inf
        for ind in inds:
            dist = (x_sp[ind] - x) ** 2 + ratio * (y_sp[ind] - y) ** 2
            if dist < dist_min:
                dist_min, ind_min = dist, ind

        model_name = self.model.get()
        self.current_spectrum.add_model(model_name, ind=ind_min)
        self.current_spectrum.result_fit = None

        self.tabview.update()
        self.plot()

    def del_peaks_point(self, x, _):
        """ Delete the closest peak 'x'-point """
        if len(self.current_spectrum.models) > 0:
            dist_min = np.inf
            for i, model in enumerate(self.current_spectrum.models):
                x0 = model.param_hints["x0"]["value"]
                dist = abs(x0 - x)
                if dist < dist_min:
                    dist_min, ind_min = dist, i
            self.current_spectrum.del_model(ind_min)
            self.current_spectrum.result_fit = None

        self.tabview.update()
        self.plot()

    def auto_peaks(self, model_name=None):
        """ Define peaks (spectrum models) from automatic detection """
        if model_name is None:
            model_name = self.model.get()
        self.current_spectrum.auto_peaks(model_name)
        self.tabview.update()
        self.tabview.update_stats()
        self.plot()

    def update_fit_settings(self):
        """ Update fit settings """
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        self.fit_settings.update(x, y)

    def colorize_from_fit_status(self, fnames=None):
        """ Colorize the fileselector items from the fit success status """
        if fnames is None:
            fnames = self.fileselector.filenames[0]

        for fname in fnames:
            ind_fselector = self.fileselector.filenames[0].index(fname)
            spectrum, _ = self.spectra.get_objects(fname)
            result_fit = spectrum.result_fit
            if result_fit is None:
                color = 'white'
            elif result_fit.success:
                color = 'Lime'
            else:
                color = 'Orange'
            self.fileselector.lbox[0].itemconfig(ind_fselector, {'bg': color})

    def fit(self, fnames=None):
        """ Fit the peaks (spectrum models) """
        if len(self.current_spectrum.models) == 0:
            return

        if fnames is None:
            fselector = self.fileselector
            fnames = fselector.filenames[0]
            fnames = [fnames[i] for i in fselector.lbox[0].curselection()]

        models = self.current_spectrum.models
        params = self.fit_settings.params
        fit_negative = params['fit_negative_values'].get() == 'On'
        max_ite = params['maximum_iterations'].get()
        fit_method = params['fit_method'].get()

        spectra = []
        bkg_model = self.bkg_model.get()
        for fname in fnames:
            spectrum, _ = self.spectra.get_objects(fname)
            spectrum.bkg_model = None if bkg_model == 'None' else bkg_model
            spectra.append(spectrum)

        ncpus = self.get_ncpus(nfiles=len(spectra))

        if ncpus == 1:
            for spectrum in spectra:
                spectrum.models = deepcopy(models)
                spectrum.fit(fit_method, fit_negative, max_ite)
        else:
            fit_mp(spectra, models, fit_method, fit_negative, max_ite, ncpus)

        self.colorize_from_fit_status(fnames=fnames)
        self.tabview.update()
        self.tabview.update_stats()
        self.plot()

    def fit_all(self):
        """ Fit the peaks (spectrum models) for all the spectra """
        self.fit(fnames=self.spectra.fnames)

    def set_spectrum_range(self, delete_tabview=True):
        """ Set range to the current spectrum """
        self.current_spectrum.range_min = float(self.range_min.get())
        self.current_spectrum.range_max = float(self.range_max.get())
        self.current_spectrum.load_profile(self.current_spectrum.fname)
        self.set_range()
        self.remove(delete_tabview=delete_tabview)

    def set_range(self):
        """ Set range from the spectrum to the appli """
        self.range_min.set(self.current_spectrum.x[0])
        self.range_max.set(self.current_spectrum.x[-1])
        self.current_spectrum.peaks_calculation()

    def apply_range_to_all(self):
        """ Apply the appli range to all the spectra """
        range_min = float(self.range_min.get())
        range_max = float(self.range_max.get())
        self.range_min.set(range_min)
        self.range_max.set(range_max)

        self.show_plot = False
        current_fname = self.current_spectrum.fname
        for spectrum in self.spectra.all:
            self.current_spectrum = spectrum
            self.set_spectrum_range(delete_tabview=False)
        self.show_plot = True
        self.reassign_current_spectrum(current_fname)
        self.tabview.delete()

    def normalize(self):
        """ Normalize all spectra from maximum or attractor position """
        norm_mode = self.normalize_mode.get().split()[0]
        norm_position_ref = self.attractor_position.get()

        if norm_mode == "Attractor" and norm_position_ref == -1:
            print('you must define an attractor position >= 0')
            return

        self.show_plot = False
        current_fname = self.current_spectrum.fname
        for self.current_spectrum in self.spectra.all:
            self.current_spectrum.norm_mode = norm_mode
            self.current_spectrum.norm_position_ref = norm_position_ref
            self.current_spectrum.normalize()
            self.remove(delete_tabview=False)
        self.show_plot = True
        self.colorize_from_fit_status(fnames=self.spectra.fnames)
        self.reassign_current_spectrum(current_fname)
        self.tabview.delete()

    def reinit(self, fnames=None):
        """ Reinitialize the spectrum """
        if fnames is None:
            fselector = self.fileselector
            fnames = fselector.filenames[0]
            fnames = [fnames[i] for i in fselector.lbox[0].curselection()]

        for fname in fnames:
            spectrum, _ = self.spectra.get_objects(fname)
            spectrum.range_min = None
            spectrum.range_max = None
            spectrum.x = spectrum.x0.copy()
            spectrum.y = spectrum.y0.copy()
            spectrum.result_fit = None
            spectrum.baseline_history = []
            spectrum.remove_models()
            spectrum.baseline.points = [[], []]

        self.colorize_from_fit_status(fnames=fnames)
        self.tabview.delete()
        self.set_range()
        self.ax.clear()
        self.plot()

    def reinit_all(self):
        """ Reinitialize all the spectra """
        self.reinit(fnames=self.spectra.fnames)

    def reassign_current_spectrum(self, fname):
        """ Reassign the current spectrum from 'fname' """
        ind = self.fileselector.filenames[0].index(fname)
        self.fileselector.lbox[0].selection_clear(0, END)
        self.fileselector.lbox[0].selection_set(ind)
        self.current_spectrum, _ = self.spectra.get_objects(fname)
        self.ax.clear()
        self.plot()

    def remove(self, delete_tabview=True):
        """ Remove all the features (spectrum attributes, baseline, tabview) """
        if self.current_spectrum is not None:
            self.current_spectrum.remove_models()
            self.delete_baseline()
            if delete_tabview:  # expensive operation when doing a lot of times
                self.tabview.delete()
            self.ax.clear()
            self.plot()

    def auto_eval(self, model_name=None):
        """ Fit spectrum after evaluating baseline and peaks automatically """
        self.auto_baseline()
        self.substract_baseline(fnames=[self.current_spectrum.fname])
        self.auto_peaks(model_name=model_name)
        self.fit(fnames=[self.current_spectrum.fname])

    def auto_eval_all(self, model_name=None):
        """ Apply automatic fitting on all spectra  """
        self.show_plot = False
        current_fname = self.current_spectrum.fname
        for spectrum in self.spectra.all:
            self.current_spectrum = spectrum
            self.auto_eval(model_name=model_name)
        self.colorize_from_fit_status(self.spectra.fnames)
        self.show_plot = True
        self.reassign_current_spectrum(current_fname)

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
        fnames_fselector = fselector.filenames[0]

        if isinstance(fnames, list):
            for fname in fnames:
                if fname in fnames_fselector:
                    ind = fnames_fselector.index(fname)
                    self.fileselector.lbox[0].delete(ind)
                    self.fileselector.filenames[0].pop(ind)

        fnames_fselector = fselector.filenames[0]
        for fname_spectra in self.spectra.fnames:
            if fname_spectra not in fnames_fselector:
                spectrum, spectra = self.spectra.get_objects(fname_spectra)
                if isinstance(spectra, SpectraMap):
                    spectra.arr[spectra.index(spectrum)] = np.nan
                spectra.remove(spectrum)

        for spectra in self.spectra.spectra_maps:
            spectra.plot_map_update()

        if len(fselector.lbox[0].curselection()) == 0:
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
                if fname not in self.fileselector.filenames[0]:
                    self.fileselector.add_items(filenames=[fname])

        # create Spectrum or SpectramMap objects associated to the new items
        fname_first_item = None
        for fname in self.fileselector.filenames[0]:
            if fname not in self.spectra.fnames:

                # 2D-map detection
                if os.path.isfile(fname):
                    with open(fname, 'r') as fid:
                        if fid.readline()[0] == "\t":
                            self.create_map(fname)
                            return

                if fname_first_item is None:
                    fname_first_item = fname

                spectrum = Spectrum()
                spectrum.load_profile(fname)
                spectrum.peaks_params = self.attractors_settings.params
                self.spectra.append(spectrum)

        self.update(fname=fname_first_item or self.fileselector.filenames[0][0])

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
            if fname not in self.fileselector.filenames[0]:
                self.fileselector.add_items(filenames=[fname])
            ind = self.fileselector.filenames[0].index(fname)
            self.fileselector.lbox[0].selection_clear(0, END)
            self.fileselector.lbox[0].selection_set(ind)
            self.fileselector.lbox[0].see(ind)
        else:
            # get fname from the first cursor selection
            curselection = self.fileselector.lbox[0].curselection()
            fname = self.fileselector.filenames[0][curselection[0]]

        if "X=" in fname:
            self.update_markers(fname)

        self.current_spectrum, _ = self.spectra.get_objects(fname)

        self.show_plot = False
        self.set_range()
        self.update_attractors()
        self.tabview.spectrum = self.current_spectrum
        self.tabview.plot = self.plot
        self.tabview.update()
        self.tabview.update_stats()
        self.show_plot = True
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
        ind = self.fileselector.filenames[0].index(fname)
        self.fileselector.lbox[0].delete(ind)
        self.fileselector.filenames[0].pop(ind)

        # add each spectra related to the 2D-map
        fnames = [spectrum.fname for spectrum in spectra_map]
        self.add_items(fnames=fnames)

        # force cursor location at the first item
        self.update(fnames[0])
