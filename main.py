import sys
import os
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer
from ui.main_window import MainWindow


def load_stylesheet(app):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    qss_path = os.path.join(script_dir, "ui", "style.qss")
    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass


def show_splash_screen():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "data", "Logo.jpg")
    pixmap = QPixmap(image_path)
    splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
    splash.show()
    QTimer.singleShot(1000, splash.close)
    return splash


if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_stylesheet(app)
    splash = show_splash_screen()
    window = MainWindow()
    window.show()
    splash.finish(window)
    sys.exit(app.exec())