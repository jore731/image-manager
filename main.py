import os, sys
from PyQt5.QtWidgets import QApplication, QStyleFactory
from view.dragToOrganizeView import dragToOrganizeView
import CommonVariables
from PyQt5.QtCore import QSize, QRect

class mainApplication(QApplication):
    def __init__(self):
        super(mainApplication,self).__init__(sys.argv)
        CommonVariables.desktopSize = QApplication.desktop().availableGeometry().size()
        self.configureSystem()
        self.execute()

    def configureSystem(self):
        self.dragToOrganizeView = dragToOrganizeView()
    
    def execute(self):
        self.dragToOrganizeView.show()
if __name__ == "__main__":
    App = mainApplication()
    # App.setStyle(QStyleFactory.create("gtk"))
    App.exec_()
    App.setQuitOnLastWindowClosed(True)
