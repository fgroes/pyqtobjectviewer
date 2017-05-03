import sys
import numpy as np
from PyQt4 import QtGui, QtCore


class StateView(QtGui.QGraphicsItem):

    def __init__(self, name, parent=None, scene=None):
        super(StateView, self).__init__(parent=parent, scene=scene)
        self.name = name
        self._bounding_rect = None
        self._transition_starts = []
        self._transition_ends = []
        self._init_ui()

    def _init_ui(self):
        scene = self.scene()
        text = QtGui.QGraphicsTextItem(self.name, parent=self, scene=scene)
        self._bounding_rect = text.boundingRect()
        rect = QtGui.QGraphicsRectItem(self._bounding_rect, parent=self, scene=scene)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)

    def boundingRect(self):
        return self._bounding_rect

    def paint(self, painter, styleOptionGraphicsItem, widget=None):
        pass

    def getTransitionPos(self):
        return self.pos()

    def add_transition_start(self, transition):
        pos = self.pos()
        transition.setStart(pos.x(), pos.y())
        self._transition_starts.append(transition)

    def add_transition_end(self, transition):
        pos = self.pos()
        transition.setEnd(pos.x(), pos.y())
        self._transition_ends.append(transition)

    def mouseMoveEvent(self, e): #QGraphicsSceneMouseEvent
        pos = self.pos()
        for t in self._transition_starts:
            t.setStart(pos.x(), pos.y())
        for t in self._transition_ends:
            t.setEnd(pos.x(), pos.y())
        super(StateView, self).mouseMoveEvent(e)


class TransitionView(QtGui.QGraphicsItem):

    def __init__(self, start_state, end_state, parent=None, scene=None):
        super(TransitionView, self).__init__(parent=parent, scene=scene)
        self._start_state = start_state
        self._end_state = end_state
        self._init_ui()

    def _init_ui(self):
        scene = self.scene()
        pos1 = self._start_state.getTransitionPos()
        pos2 = self._end_state.getTransitionPos()
        self.line = QtGui.QGraphicsLineItem(0.0, 0.0, 1.0, 1.0, scene=scene)

    def boundingRect(self):
        return self.line.boundingRect()

    def paint(self, painter, styleOptionGraphicsItem, widget=None):
        pass

    def setStart(self, x, y):
        l = self.line.line()
        self.line.setLine(x, y, l.x2(), l.y2())

    def setEnd(self, x, y):
        l = self.line.line()
        self.line.setLine(l.x1(), l.y1(), x, y)


class MyTest(QtGui.QGraphicsView):
    def __init__(self, states, transitions, parent=None):
        super(MyTest, self).__init__(parent)
        self.states = states
        self.transitions = transitions
        self._state_views = {}
        self._transition_views = []
        self._init_ui()

    def _init_ui(self):
        scene = QtGui.QGraphicsScene()
        self.setScene(scene)
        radius = 100
        n = len(self.states)
        for i, name in enumerate(self.states):
            sv = StateView(name, scene=scene)
            angle = 2 * np.pi / n * i - np. pi / 2
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            sv.setPos(x, y)
            self._state_views[name] = sv
        for trans in self.transitions:
            start_state = self._state_views[trans[0]]
            end_state = self._state_views[trans[1]]
            t = TransitionView(start_state, end_state, scene=scene)
            start_state.add_transition_start(t)
            end_state.add_transition_end(t)
            self._transition_views.append(t)
        #self.setInteractive(True)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    states = ["Idle", "Doing", "Done"]
    transitions = [("Idle", "Doing"), ("Doing", "Done"), ("Done", "Idle")]
    test = MyTest(states, transitions)
    test.show()
    sys.exit(app.exec_())
