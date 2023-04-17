import faulthandler

import enaml
from enaml.qt.qt_application import QtApplication

import enamlx


def main():
    # Install the enamlx tools
    enamlx.install()
    # Enable fault handling
    faulthandler.enable()
    with enaml.imports():
        from table_view import TableStart
    # Create a new `QtApplication` object
    app = QtApplication()
    # Create a new `TableStart` view object
    view = TableStart()
    # Show the view
    view.show()
    # Start the application
    app.start()



if __name__ == "__main__":
    main()