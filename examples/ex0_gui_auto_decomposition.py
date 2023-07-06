"""
Example of 'GUI' spectra automatic decomposition
"""
import os
import tkinter as tk

from fitspy.app.gui import Appli

root = tk.Tk()
appli = Appli(root)

# specify the dirname to work with
dirname = os.path.join('data', 'spectra_1')
appli.add_items_from_dir(dirname=dirname)

# all spectra automatic processing (baseline and peaks evaluation + fitting)
appli.auto_eval_all()

root.mainloop()
