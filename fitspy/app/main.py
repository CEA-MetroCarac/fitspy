import sys
from PySide6.QtWidgets import QApplication
from fitspy.app import MainController
from fitspy.app import MainModel
from fitspy.app import MainView

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    model = MainModel()
    view = MainView()
    main_controller = MainController(model, view)
    main_controller.view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()