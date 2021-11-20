import os
import subprocess
import sys

from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QProgressBar, QVBoxLayout, QPushButton, QFileDialog, QApplication, QCheckBox, QSpinBox, \
    QMessageBox

from coders.caesar import CaesarEncryptor, CaesarDecryptor


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.setWindowFlag(QtCore.Qt.WindowMinMaxButtonsHint, False)
        self.setWindowTitle("Encoder | Decoder | By MaxP")

        self.out_path = ''
        self.progress_callback = self.on_progress

        btn_style = 'font-size: 24px'

        self.encode_btn = QPushButton('Encode')
        self.decode_btn = QPushButton('Decode')
        self.encode_btn.setStyleSheet(btn_style)
        self.decode_btn.setStyleSheet(btn_style)

        self.encode_btn.clicked.connect(self.encode)
        self.decode_btn.clicked.connect(self.decode)

        self.draw_progress_bar_checkbox = QCheckBox('Draw progress bar (slower)')
        self.draw_progress_bar_checkbox.setChecked(True)
        self.draw_progress_bar_checkbox.stateChanged.connect(self.draw_progress_bar_checked)

        self.encryption_key = QSpinBox()
        self.encryption_key.setMinimum(0)
        self.encryption_key.setMaximum(10000)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(QtCore.Qt.AlignHCenter)

        self.layout = QVBoxLayout(self)

        self.layout.addStretch()
        self.layout.addWidget(self.encode_btn)
        self.layout.addWidget(self.decode_btn)
        self.layout.addWidget(self.encryption_key)
        self.layout.addWidget(self.draw_progress_bar_checkbox)
        self.layout.addWidget(self.progress_bar)
        self.layout.addStretch()

    def encode(self):
        dialog = QFileDialog()
        path = dialog.getOpenFileName(self, 'Select a file to compress', filter='Text file (*.txt)')[0]

        if not path:
            return

        filename = os.path.basename(path) + '.prar'

        self.out_path = dialog.getSaveFileName(self, 'Select where to save file', os.path.join('./out', filename))[0]

        if not self.out_path:
            return

        with open(path, 'r', encoding='utf-8', newline='\n') as file_in:
            with open(self.out_path, 'wb') as file_out:
                CaesarEncryptor(file_in, file_out, self.progress_callback).write()
        self.on_finish('OK')

    def decode(self):
        dialog = QFileDialog()
        path = dialog.getOpenFileName(self, 'Select a file to uncompress', filter='Pum rar (*.prar)')[0]

        if not path:
            return

        filename = os.path.basename(path).replace('.prar', '')

        self.out_path = dialog.getSaveFileName(self, 'Select where to save file', os.path.join('./out', filename))[0]

        if not self.out_path:
            return

        with open(path, 'rb') as file_in:
            with open(self.out_path, 'w', encoding='utf-8', newline='\n') as file_out:
                CaesarDecryptor(file_in, file_out, self.progress_callback).read()
        self.on_finish('OK')

    def on_progress(self, total, processed):
        if self.progress_bar.maximum() != total:
            self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(processed)

        if processed % 100:
            QApplication.processEvents()

    def on_finish(self, msg: str):
        if msg != 'OK':
            msg_box = QMessageBox(QMessageBox.Warning, 'Error while reading\\writing', msg)
            msg_box.exec()
            return
        else:
            self.out_path = self.out_path.replace('/', '\\')
            subprocess.Popen(f'explorer /select,"{self.out_path}"')

        self.progress_bar.setValue(0)

    def draw_progress_bar_checked(self, event):
        self.progress_callback = self.on_progress if self.draw_progress_bar_checkbox.isChecked() else None


if __name__ == "__main__":
    if not os.path.exists('out'):
        os.makedirs('out')

    app = QtWidgets.QApplication([])

    widget = MainWidget()
    widget.resize(200, 200)
    widget.show()

    sys.exit(app.exec())
