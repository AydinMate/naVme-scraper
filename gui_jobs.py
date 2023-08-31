import customtkinter
from tkcalendar import Calendar
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv
import os
from address_finder import AddressFinder
from volume_finder import VolumeFinder
from scraper import Scrape
import asyncio

scraper = Scrape

async def scrape_data(date):  # date argument added
    parts = date.split("-")  # Split the date into year, month, and day parts
    month = parts[1].lstrip("0")  # Remove leading zeros from the month
    day = parts[2].lstrip("0")  # Remove leading zeros from the day
    formatted_date = f"{parts[0]}-{month}-{day}"  # Reconstruct the formatted date
    print("Formatted Date:", formatted_date)
    print(f"Scraping data for date: {formatted_date}")

    url = os.getenv("PROVANS_WEBSITE")
    scraper = Scrape(url, formatted_date)
    return await scraper.scrape_orders()

class CalendarFrame(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title_label = customtkinter.CTkLabel(self, text=title, fg_color="gray30", corner_radius=6)
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.selected_date = customtkinter.StringVar(value=datetime.now().date())

        self.calendar = Calendar(
            self,
            mindate=(datetime.now() - timedelta(days=365)).date(),
            maxdate=(datetime.now() + timedelta(days=7)).date()
        )
        self.calendar.grid(row=1, column=0, pady=(100, 0))
        self.calendar.bind("<<CalendarSelected>>", self.update_date_label)
        
        self.info_frame = customtkinter.CTkFrame(self,)
        self.info_frame.grid(row=2, column=0, padx=10, pady=(0, 10))

        self.selected_label = customtkinter.CTkLabel(
            self.info_frame,
            text="Selected Date: "
        )
        self.selected_label.grid(row=0, column=0, sticky="w")

        self.date_label = customtkinter.CTkLabel(
            self.info_frame,
            textvariable=self.selected_date
        )
        self.date_label.grid(row=0, column=1, sticky="w")

    def update_date_label(self, event):
        selected_date = self.calendar.selection_get()
        self.selected_date.set(selected_date.strftime('%Y-%m-%d'))



class InformationFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, steps):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.steps = steps
        self.title_label = customtkinter.CTkLabel(self, text=title, fg_color="gray30", corner_radius=6)
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.variable = customtkinter.StringVar(value="")

        self.radiobuttons = []
        for i, step in enumerate(self.steps):
            radiobutton = customtkinter.CTkRadioButton(self, text=step, value=step, variable=self.variable)
            radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.radiobuttons.append(radiobutton)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('naVme Desktop')
        self.geometry('1280x720')
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1280) // 2
        y = (screen_height - 720) // 2
        self.geometry(f'1280x720+{x}+{y}')
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.calendar_frame = CalendarFrame(self, "Pick a date")
        self.calendar_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.radiobutton_frame = InformationFrame(self, "Progress", steps=["option 1", "option 2"])
        self.radiobutton_frame.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew")

        self.button = customtkinter.CTkButton(self, text="Find and Send Jobs", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def button_callback(self):
        print("Selected Date:", self.calendar_frame.selected_date.get())

        loop = asyncio.get_event_loop()
        

        database_jobs = loop.run_until_complete(scrape_data(self.calendar_frame.selected_date.get()))

        load_dotenv()

        google_maps_api_key = os.getenv("GOOGLE_MAPS_API")


        api_key = google_maps_api_key

        job_formatter = AddressFinder(api_key)
        database_jobs = job_formatter.format_job_details(database_jobs)

        volume_finder = VolumeFinder(database_jobs)
        volume_finder.get_updated_jobs()
        volume_finder.save_to_file()




