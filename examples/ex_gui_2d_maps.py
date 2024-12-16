# DONE
"""
Example of 2D maps loading
"""
from pathlib import Path
from PySide6.QtWidgets import QApplication

from fitspy.app import MainController, MainModel, MainView

DATA = Path(__file__).parent / "data"

def gui_2d_maps(dirname_res=None):
    """ Example of 2D maps loading """
    app = QApplication([])
    app.setStyle("Fusion")
    model = MainModel()
    view = MainView()
    main_controller = MainController(model, view)

    # specify the dirname to work with
    str_map = str(DATA / '2D_maps' / 'ordered_map.txt')
    unstr_map = str(DATA / '2D_maps' / 'unordered_map.txt')
    main_controller.open(fnames=[str_map, unstr_map])

    # main_controller.remove_outliers() # spectra from the maps differ: DO NOT APPLY

    # automatic evaluation on the first 5 spectra

    # save and destroy for pytest
    if dirname_res is not None:
        list_widget = view.spectrum_list.list
        fnames = [list_widget.item(i).text() for i in range(list_widget.count())]
        main_controller.save_results(dirname_res=dirname_res, fnames=fnames)
        return

    main_controller.view.show()
    app.exec()


if __name__ == "__main__":
    gui_2d_maps()