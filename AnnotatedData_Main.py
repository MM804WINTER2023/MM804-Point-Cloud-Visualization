import faulthandler

import enaml
from enaml.qt.qt_application import QtApplication

import enamlx


def runTable():
    enamlx.install()

    faulthandler.enable()
    with enaml.imports():
        from table_view import TableView

    app = QtApplication()
    view = TableView()
    view.show()

    app.start()


