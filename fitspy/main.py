import sys
from PySide6.QtWidgets import QApplication
from controllers.controller import Controller

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_controller = Controller()
    main_controller.view.show()  # Show the view directly
    sys.exit(app.exec())
