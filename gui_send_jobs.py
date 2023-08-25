from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout,
                             QCalendarWidget, QHBoxLayout)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QDate, Qt

import asyncio
import data_handler

class SendJobsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Vertical layout for the entire widget
        main_layout = QVBoxLayout()

        # Set padding around the main layout
        main_layout.setContentsMargins(100, 100, 100, 100)  # left, top, right, bottom
        
        # Title Label
        label = QLabel("Send Jobs", self)
        label.setFont(QFont("Arial", 24))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(label)

        # Horizontal layout for calendar and status message
        calendar_and_status_layout = QHBoxLayout()

        # Calendar and its title in a vertical layout
        calendar_layout = QVBoxLayout()

        # Calendar title centered above the calendar
        calendar_title = QLabel("Select Date", self)
        calendar_title.setFont(QFont("Arial", 18))
        calendar_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        calendar_layout.addWidget(calendar_title)

        # Calendar
        self.calendar = QCalendarWidget(self)
        self.calendar.setFixedSize(350, 200)
        tomorrow = QDate.currentDate().addDays(1)
        self.calendar.setSelectedDate(tomorrow)
        self.calendar.selectionChanged.connect(self.update_selected_date)
        calendar_layout.addWidget(self.calendar)
        calendar_layout.setContentsMargins(0, 0, 0, 100)

        calendar_and_status_layout.addLayout(calendar_layout)

        # Status Label on the right of the calendar
        self.status_label = QLabel(self)
        self.status_label.setFont(QFont("Arial", 24))
        self.status_label.setStyleSheet("color: black")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        calendar_and_status_layout.addWidget(self.status_label)

        # Add calendar and status layout to the main layout
        main_layout.addLayout(calendar_and_status_layout)

        # Selected date feedback label
        self.selected_date_label = QLabel(f"Selected Date: {tomorrow.toString('dd MMM yyyy')}", self)
        self.selected_date_label.setFont(QFont("Arial", 14))
        main_layout.addWidget(self.selected_date_label)

        # Send button
        send_button = QPushButton("Fetch and Send Data", self)
        send_button.setFont(QFont("Arial", 14))
        send_button.clicked.connect(self.on_send_clicked)
        main_layout.addWidget(send_button)

        # Set main layout to the widget
        self.setLayout(main_layout)

    def update_selected_date(self):
        selected_date = self.calendar.selectedDate().toString("dd MMM yyyy")
        self.selected_date_label.setText(f"Selected Date: {selected_date}")

    def on_send_clicked(self):
        # Set status label to fetching before starting the scrape
        self.status_label.setText("Fetching...")
        self.repaint()  # Ensures that the GUI updates before proceeding

        # Scrape data based on selected date
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        
        loop = asyncio.get_event_loop()
        data = loop.run_until_complete(data_handler.scrape_data(date=selected_date))

        # Send data
        result = data_handler.send_data_to_endpoint(data)

        # Extract the message and status code from the result tuple
        message, status_code = result 

        # Update status label based on response
        if status_code == 200:
            self.status_label.setText(message)
            self.status_label.setStyleSheet("color: green")
        else:
            self.status_label.setText(f"Error: {message}")
            self.status_label.setStyleSheet("color: red")
