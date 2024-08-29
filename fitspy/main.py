import sys
from PySide6.QtWidgets import QApplication
from app.main_controller import MainController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_controller = MainController()
    main_controller.view.show()
    sys.exit(app.exec())
