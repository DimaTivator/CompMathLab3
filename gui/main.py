import traceback

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from functions import *
from compmath.calc import *
from compmath.nonlinear import *
from compmath.plot import plot_function

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


functions_buttons = {
    'f1_button': f1,
    'f2_button': f2,
    'f3_button': f3,
    'f4_button': f4,
    'f5_button': f5,
}

methods_buttons = {
    'rect_left_button': left_rectangles,
    'rect_right_button': right_rectangles,
    'rect_mid_button': midpoint_rectangles,
    'trap_button': trapezoidal,
    'simpson_button': simpson
}

function = f1
method = left_rectangles
a = 0
b = 0
n = 4
eps = 0.01


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        uic.loadUi("main.ui", self)

        self.f_buttons = [
            self.f1_button,
            self.f2_button,
            self.f3_button,
            self.f4_button,
            self.f5_button
        ]

        self.m_buttons = [
            self.rect_left_button,
            self.rect_mid_button,
            self.rect_right_button,
            self.trap_button,
            self.simpson_button
        ]

        self.line_edits = [
            self.a_line_edit,
            self.b_line_edit,
            self.eps_line_edit
        ]

        self.plot_widget = FigureCanvas(plt.figure())

        self.show()
        self.initUI()

    def initUI(self):
        self.load_function_imgs()

        for button in self.f_buttons:
            button.clicked.connect(self.f_radio_button_clicked)

        for button in self.m_buttons:
            button.clicked.connect(self.method_radio_button_clicked)

        validator = QRegExpValidator(QRegExp("[+-]?\\d*\\.?\\d+"))

        for line_edit in self.line_edits:
            line_edit.setValidator(validator)
            line_edit.setText('0')

        self.eps_line_edit.setText('0.01')

        self.solve_button.clicked.connect(self.solve)

    def f_radio_button_clicked(self):
        global function

        sender = self.sender()
        if sender.isChecked():
            function = functions_buttons[sender.objectName()]

    def method_radio_button_clicked(self):
        global method

        sender = self.sender()
        if sender.isChecked():
            method = methods_buttons[sender.objectName()]

    def load_function_imgs(self):
        pixmap = QPixmap("img/functions/f1.png")
        self.f1_label.setPixmap(pixmap)
        self.f1_label.setScaledContents(True)

        pixmap = QPixmap("img/functions/f2.png")
        self.f2_label.setPixmap(pixmap)
        self.f2_label.setScaledContents(True)

        pixmap = QPixmap("img/functions/f3.png")
        self.f3_label.setPixmap(pixmap)
        self.f3_label.setScaledContents(True)

        pixmap = QPixmap("img/functions/f4.png")
        self.f4_label.setPixmap(pixmap)
        self.f4_label.setScaledContents(True)

        pixmap = QPixmap("img/functions/f5.png")
        self.f5_label.setPixmap(pixmap)
        self.f5_label.setScaledContents(True)

    def parse_params(self):
        global a, b, eps

        values = []
        for line_edit in self.line_edits:
            values.append(float(line_edit.text().replace(',', '.')))

        a, b, eps = values

        if eps <= 0 or a >= b:
            raise ValueError

    def draw_plot(self):

        fig = plot_function(function, a - 2, b + 2)

        canvas = FigureCanvas(fig)

        pixmap = QPixmap(canvas.size())
        canvas.render(pixmap)

        self.plot_label.setPixmap(pixmap)
        self.plot_label.setScaledContents(True)

    def fill_table(self, log):
        num_rows = len(log)
        num_cols = len(log[0])

        self.history_table.setStyleSheet("QTableWidget::item:selected { background-color: lightgray; }")

        self.history_table.setRowCount(num_rows)
        self.history_table.setColumnCount(num_cols)

        self.history_table.setHorizontalHeaderLabels(log[0])

        for i, line in enumerate(log[1:]):
            for j, value in enumerate(line):
                try:
                    val = "{:.8f}".format(float(value))
                except ValueError:
                    val = str(value)
                item = QTableWidgetItem(val)
                self.history_table.setItem(i, j, item)

    def solve(self):
        try:
            self.parse_params()
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Invalid parameters a, b or eps')
            return

        self.draw_plot()

        try:
            log = method(function, a, b, eps)
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Invalid segment [a, b]. Check the domain of the chosen function')
            return

        self.fill_table(log)


def main():
    app = QApplication([])
    window = App()

    app.exec_()


if __name__ == '__main__':
    main()

