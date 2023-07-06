"""
Example of spectra fitting through the GUI and a model applied to all
"""
import os
import tkinter as tk

from fitspy.app.gui import Appli

root = tk.Tk()
appli = Appli(root)

# specify the dirname to work with
dirname = os.path.join('data', 'spectra_2')
appli.add_items_from_dir(dirname=dirname)

# load model and apply it to ALL SPECTRA
fname_json = os.path.join(dirname, 'model.json')
model = appli.load_model(fname_json=fname_json)
appli.apply_model(model)

# canvas rescaling
appli.rescale()

# save results and figures
# appli.save_results(dirname_res='results')
# appli.save_figures(dirname_fig='results')

root.mainloop()
