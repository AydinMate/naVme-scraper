from PyQt6.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout
from gui_send_jobs import SendJobsWidget
from gui_settings import SettingsWidget

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create Tab Control
        tabControl = QTabWidget(self)
        
        # Add tabs
        tabControl.addTab(SendJobsWidget(), "Send Jobs")
        tabControl.addTab(SettingsWidget(), "Settings")

        layout.addWidget(tabControl)
        self.setLayout(layout)

def app_exec():
    app = QApplication([])
    window = MainApp()
    window.setGeometry(320, 180, 1280, 720)
    window.setWindowTitle("naVme Desktop")
    window.show()
    app.exec()

if __name__ == '__main__':
    app_exec()

