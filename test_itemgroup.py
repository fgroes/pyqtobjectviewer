import sys
import numpy as np
from PyQt4 import QtGui, QtCore


class MyTest(QtGui.QGraphicsView):
    def __init__(self, state_views, parent=None):
        super(MyTest, self).__init__(parent)
        self.state_views = state_views
        self._init_ui()
        self.draw_scene()

    def _init_ui(self):
        scene = QtGui.QGraphicsScene()
        self.setScene(scene)
        group = QtGui.QGraphicsItemGroup()
        scene.addItem(group)
        text = scene.addText("Test")
        group.addToGroup(text)
        br = text.boundingRect()
        rect = scene.addRect(br)
        group.addToGroup(rect)
        group.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setInteractive(True)

    def draw_scene(self):
        r = 100
        n = len(self.state_views)
        for i, sv in enumerate(self.state_views):
            sv.scene = self.scene()
            x = r * np.cos(2 * np.pi / n * i)
            y = r * np.sin(2 * np.pi / n * i)
            sv.pos = (x, y)
            sv.draw()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    state_views = [ ]
    test = MyTest(state_views)
    test.show()
    sys.exit(app.exec_())
