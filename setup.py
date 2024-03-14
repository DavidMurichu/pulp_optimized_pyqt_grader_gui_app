
from imports import QApplication, QMessageBox, psutil, platform, subprocess, sys

def show_dialog(message):
    app = QApplication([])
    message_box = QMessageBox()
    message_box.setWindowTitle("Database error")
    message_box.setText(f"{message}")
    message_box.exec()







