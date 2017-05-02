import sys
import numpy as np
from PyQt4 import QtGui, QtCore


class StateGraphicsItem(QtGui.QGraphicsItemGroup):

    def mouseMoveEvent(self, e):
        print(e.pos())
        p = e.pos()
        l = self.line.line()
        self.line.setLine(p.x(), p.y(), l.x2(), l.y2())
        super(StateGraphicsItem, self).mouseMoveEvent(e)

    def addTransition(self, line):
        self.line = line


class StateView(object):

    def __init__(self, name, scene=None):
        self.scene = scene
        self.name = name
        self.pos = (0, 0)

    def draw(self):
        if not self.scene: return
        group = StateGraphicsItem()
        line = self.scene.addLine(0, 0, 30, 30)
        group.addTransition(line)
        self.scene.addItem(group)
        name_text = self.scene.addText(self.name)
        group.addToGroup(name_text)
        #name_text.setPos(*self.pos)
        br = name_text.boundingRect()
        self.bounding_rect = self.scene.addRect(br)
        group.addToGroup(self.bounding_rect)
        group.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        group.setPos(*self.pos)


class MyTest(QtGui.QGraphicsView):
    def __init__(self, state_views, parent=None):
        super(MyTest, self).__init__(parent)
        self.state_views = state_views
        self._init_ui()
        self.draw_scene()

    def _init_ui(self):
        scene = QtGui.QGraphicsScene()
        self.setScene(scene)
        #self.setInteractive(True)

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
    state_views = [StateView("Idle"), StateView("Doing"), StateView("Done")]
    test = MyTest(state_views)
    test.show()
    sys.exit(app.exec_())
