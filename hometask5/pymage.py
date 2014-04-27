__author__ = 'inaumov'

import sys
import PySide
from PySide.QtGui import *

class PymageViewer(QWidget):
    def __init__(self):
        super(PymageViewer, self).__init__()
        self.initUI()

    def initUI(self):
        self.zoomMult = 1
        self.pixMap = None

        self.setFixedSize(500, 500)
        self.setWindowTitle('PyMage')

        self.openImageButton = QPushButton()
        self.openImageButton.setText('Open image')
        self.openImageButton.clicked.connect(self.showFileDialog)

        self.zoomInButton = QPushButton()
        self.zoomInButton.setText('Zoom in')
        self.zoomInButton.clicked.connect(self.zoomIn)

        self.zoomOutButton = QPushButton()
        self.zoomOutButton.setText('Zoom out')
        self.zoomOutButton.clicked.connect(self.zoomOut)

        self.toolbar = QToolBar(self)
        self.toolbar.setFixedSize(500, 30)

        self.toolbar.addWidget(self.openImageButton)
        self.toolbar.addWidget(self.zoomInButton)
        self.toolbar.addWidget(self.zoomOutButton)

        self.show()
        return 0

    def showFileDialog(self):
        filePath = QFileDialog.getOpenFileName(self, 'Open image:', '', 'Image files (*.png *.jpg)')[0]

        if filePath is None or filePath == '':
            return

        self.pixMap = QPixmap(filePath)

        scene = QGraphicsScene()
        scene.addPixmap(self.pixMap)

        viewer = QGraphicsView(self)
        viewer.setScene(scene)
        viewer.setFixedSize(500, 460)
        viewer.move(0, 40)
        viewer.show()

    def zoomIn(self):
        if not self.pixMap is None:
            if (self.zoomMult < 4):
                self.zoomMult = self.zoomMult * 1.25
            self.refreshImage()

    def zoomOut(self):
        if not self.pixMap is None:
            if (self.zoomMult > 0.075):
                self.zoomMult = self.zoomMult * 0.75
            self.refreshImage()

    def refreshImage(self):
        scene = QGraphicsScene()
        scene.addPixmap(self.pixMap.scaled(self.pixMap.size() * self.zoomMult))

        viewer = QGraphicsView(self)
        viewer.setScene(scene)
        viewer.setFixedSize(500, 460)
        viewer.move(0, 40)
        viewer.show()

def main():
    app = QApplication(sys.argv)
    viewer = PymageViewer()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()