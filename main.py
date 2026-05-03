import sys
import os
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont
from PySide6.QtCore import Qt, QTimer
from ui.main_window import MainWindow
from company_config import COMPANY, get_logo_path
from version import APP_VERSION


def load_stylesheet(app):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    qss_path = os.path.join(script_dir, "ui", "style.qss")
    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass


def show_splash_screen():
    pixmap = QPixmap(get_logo_path())
    if pixmap.isNull():
        pixmap = QPixmap(400, 200)
        pixmap.fill(QColor("#2C5F8A"))

    # Affiche la version en bas à droite du splash
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    font = QFont("Segoe UI", 9)
    painter.setFont(font)
    painter.setPen(QColor("#FFFFFF"))
    painter.drawText(
        pixmap.rect().adjusted(0, 0, -8, -6),
        Qt.AlignBottom | Qt.AlignRight,
        f"v{APP_VERSION}"
    )
    painter.end()

    splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
    splash.show()
    QTimer.singleShot(1000, splash.close)
    return splash


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName(COMPANY["name"])
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName(COMPANY.get("legal", COMPANY["name"]))

    load_stylesheet(app)
    splash = show_splash_screen()
    window = MainWindow()
    window.show()
    splash.finish(window)
    sys.exit(app.exec())
