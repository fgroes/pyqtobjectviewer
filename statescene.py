import sys
import numpy as np
from PyQt4 import QtGui, QtCore


class StateWidget(QtGui.QWidget):

    moved = QtCore.pyqtSignal(str, int, int)

    def __init__(self, name, parent=None):
        super(StateWidget, self).__init__(parent)
        self._name = name
        self._init_ui()
        self._mouse_press_pos = None

    def _init_ui(self):
        l = QtGui.QVBoxLayout()
        self.setLayout(l)
        nl = QtGui.QLabel(self._name)
        l.addWidget(nl)

    def mousePressEvent(self, e):
        self._mouse_press_pos = None
        self._mouse_move_pos = None
        if e.buttons() == QtCore.Qt.LeftButton:
            self._mouse_press_pos = e.globalPos()
            self._mouse_move_pos = e.globalPos()

    def mouseMoveEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:
            curr_pos = self.mapToGlobal(self.pos())
            mouse_pos = e.globalPos()
            mouse_diff = mouse_pos - self._mouse_move_pos
            new_pos = self.mapFromGlobal(curr_pos + mouse_diff)
            self.move(new_pos)
            self._mouse_move_pos = mouse_pos
            self.moved.emit(self._name, mouse_diff.x(), mouse_diff.y())

    def mouseReleaseEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:
            moved_len = e.globalPos() - self._mouse_press_pos
            if moved_len.manhattanLength() > 3:
                e.ignore()
                return


class StateScene(QtGui.QGraphicsView):
    def __init__(self, states, transitions, parent=None):
        super(StateScene, self).__init__(parent)
        self._states = states
        self._states_dict = {}
        self._transitions = transitions
        self._transition_source_dict = {}
        self._transition_target_dict = {}
        self._init_ui()

    def _init_ui(self):

        scene = QtGui.QGraphicsScene()
        self.setScene(scene)

        #pen   = QtGui.QPen(QtGui.QColor(QtCore.Qt.green))
        #brush = QtGui.QBrush(pen.color().darker(150))
        r = 200
        dangle = 2 * np.pi / len(self._states)

        for i, state in enumerate(self._states):
            sw = StateWidget(state)
            sw.moved.connect(self.on_state_moved)
            ssw = scene.addWidget(sw)
            px = r * np.cos(dangle * i) - sw.width() / 2
            py = r * np.sin(dangle * i) - sw.height() / 2
            sw.move(px, py)
            self._states_dict[state] = ssw

        for transitions in self._transitions:
            source_sw = self._states_dict[transitions[0]]
            target_sw = self._states_dict[transitions[1]]
            source_pos = source_sw.pos()
            target_pos = target_sw.pos()
            x1 = source_sw.x() + source_sw.widget().width() / 2
            y1 = source_sw.y() + source_sw.widget().height() / 2
            x2 = target_sw.x() + target_sw.widget().width() / 2
            y2 = target_sw.y() + target_sw.widget().height() / 2
            line = scene.addLine(x1, y1, x2, y2)
            if transitions[0] not in self._transition_source_dict:
                self._transition_source_dict[transitions[0]] = []
            self._transition_source_dict[transitions[0]].append(line)
            if transitions[1] not in self._transition_target_dict:
                self._transition_target_dict[transitions[1]] = []
            self._transition_target_dict[transitions[1]].append(line)

        self.show()

    def on_state_moved(self, name, x, y):
        name = str(name)
        if name in self._transition_source_dict:
            for line in self._transition_source_dict[name]:
                l = line.line()
                new_l = QtCore.QLineF(l.x1() + x, l.y1() + y, l.x2(), l.y2())
                line.setLine(new_l)
        if name in self._transition_target_dict:
            for line in self._transition_target_dict[name]:
                l = line.line()
                new_l = QtCore.QLineF(l.x1(), l.y1(), l.x2() + x, l.y2() + y)
                line.setLine(new_l)


if  __name__ == '__main__' :
    states = ["Idle", "Processing", "Done"]
    transitions = [("Idle", "Processing"), ("Processing", "Done"), ("Done", "Idle")]
    app = QtGui.QApplication(sys.argv)
    ss = StateScene(states, transitions)
    app.exec_()
