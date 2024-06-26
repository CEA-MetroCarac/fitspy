# TODO snake_case everywhere or camelCase everywhere ? Python is snake_case, Qt is camelCase. from __feature__ import snake_case
import sys
from PySide6.QtWidgets import QApplication
from controllers import Controller

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_controller = Controller()
    main_controller.view.show()  # Show the view directly
    sys.exit(app.exec())
