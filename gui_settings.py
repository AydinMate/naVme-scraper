from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("DMS Settings", self)
        self.email_label = QLabel("Email:", self)
        self.email_input = QLineEdit(self)
        
        self.password_label = QLabel("Password:", self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.save_button = QPushButton("Save", self)
        # Connect save button to a function if needed
        # self.save_button.clicked.connect(self.on_save_clicked)

        layout.addWidget(self.title_label)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    # Uncomment and fill this function if you want a save functionality
    # def on_save_clicked(self):
    #     pass
