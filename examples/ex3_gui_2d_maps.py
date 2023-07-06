"""
Example of 2D maps loading
"""
import os
import tkinter as tk

from fitspy.app.gui import Appli

root = tk.Tk()
appli = Appli(root)

# specify the dirname to work with
str_map = os.path.join('data', '2D_maps', 'ordered_map.txt')
unstr_map = os.path.join('data', '2D_maps', 'unordered_map.txt')
appli.add_items(fnames=[str_map, unstr_map])

# # canvas rescaling
# appli.rescale()


root.mainloop()
