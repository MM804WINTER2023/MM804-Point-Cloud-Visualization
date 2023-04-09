import faulthandler

import enaml
from enaml.qt.qt_application import QtApplication

import enamlx


def main():
    enamlx.install()

    faulthandler.enable()
    with enaml.imports():
        from table_view import TableStart

    app = QtApplication()
    view = TableStart()
    view.show()

    app.start()


if __name__ == "__main__":
    main()