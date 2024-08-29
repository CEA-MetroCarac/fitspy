import sys
from PySide6.QtWidgets import QApplication
from app.main_controller import MainController

def main():
    app = QApplication(sys.argv)
    main_controller = MainController()
    main_controller.view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()