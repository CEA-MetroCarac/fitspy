import sys
from PySide6.QtWidgets import QApplication
from controllers.controller import Controller

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_controller = Controller()
    main_controller.show()
    sys.exit(app.exec())
