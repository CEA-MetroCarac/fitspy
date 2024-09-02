import sys
from PySide6.QtWidgets import QApplication
from fitspy.app import MainController

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    main_controller = MainController()
    main_controller.view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()