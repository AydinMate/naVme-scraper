import time
from pyppeteer import launch
from dotenv import load_dotenv
import os
import calendar
import json
from table_data_extractor import TableDataExtractor

load_dotenv()

class Scrape:
    def __init__(self, url, date=None):
        self.url = url
        self.date = date
        self.viewport_options = {
            "width": 1280,
            "height": 720,
            "deviceScaleFactor": 1.0,
            "isMobile": False,
            "hasTouch": False,
            "isLandscape": False
        }

    async def scrape_orders(self):
        year, month, day = self.date.split("-")
      
        browser = await launch(headless=False)
        page = await browser.newPage()
        await page.goto(self.url)
        await page.setViewport(viewport=self.viewport_options)

        # Log in
        await page.waitForSelector('#mat-input-1')
        await page.waitForSelector('#mat-input-2')
        await page.waitForSelector('button[type="submit"]')
        
        email_input = await page.querySelector('#mat-input-1')
        await email_input.type(os.getenv("PROVANS_EMAIL"))

        password_input = await page.querySelector('#mat-input-2')
        await password_input.type(os.getenv("PROVANS_PASSWORD"))

        login_button = await page.querySelector('button[type="submit"]')
        await login_button.click()

        time.sleep(2)


        # status button
        await page.waitForSelector('mat-select[formcontrolname="status"]')
        status_button = await page.querySelector('mat-select[formcontrolname="status"]')
        await status_button.click()

        # all button
        await page.waitForSelector('#mat-option-5')
        await page.keyboard.press("ArrowUp")
        await page.keyboard.press("ArrowUp")
        await page.keyboard.press("ArrowUp")
        await page.keyboard.press("ArrowUp")
        await page.keyboard.press("Enter")


        #date
        year, month, day = self.date.split("-")
        month_name = calendar.month_name[int(month)]

        await page.waitForSelector('button[mattooltip="Pick a date"]')
        select_date_button = await page.querySelector('button[mattooltip="Pick a date"]')
        await select_date_button.click()

        await page.waitForSelector('button[aria-label="Choose month and year"]')
        year_month_button = await page.querySelector('button[aria-label="Choose month and year"]')
        await year_month_button.click()
        
        await page.waitForSelector(f'td[aria-label="{year}"]')
        year_button = await page.querySelector(f'td[aria-label="{year}"]')
        await year_button.click()

        await page.waitForSelector(f'td[aria-label="{month_name} {year}"]')
        month_button = await page.querySelector(f'td[aria-label="{month_name} {year}"]')
        await month_button.click()

        await page.waitForSelector(f'td[aria-label="{day} {month_name} {year}"]')
        day_button = await page.querySelector(f'td[aria-label="{day} {month_name} {year}"]')
        await day_button.click()

        time.sleep(1)

        #orders
        all_orders = []
        await page.waitForSelector('mat-card[class="mdcard-unschedule-card mat-card ng-star-inserted"]')

        orders = await page.querySelectorAll('mat-card[class="mdcard-unschedule-card mat-card ng-star-inserted"]')

        for order in orders:
            time.sleep(0.5)
            status_container = await order.querySelector('h4')
            status = (await page.evaluate('(element) => element.textContent', status_container)).strip()

            if status == "DELETED":
                continue
            else:
                await order.click(clickCount=2)
                
                order_containers = await page.xpath("//div[contains(text(), 'Order :')]/following::input[1]")
                if order_containers:
                    order_container = order_containers[0]
                    order_number = await page.evaluate('(element) => element.value', order_container)

                    # Dropoff Tab
                    dropoff = await page.xpath("//div[contains(@class, 'mat-tab-label-content') and contains(text(), 'Dropoff')]")
                    if dropoff:
                        await dropoff[0].click()

                        address = ""
                        counter = 0
                        while address == "" and counter < 10:
                    
                            address_containers = await page.xpath("//div[contains(text(), 'Original Address')]/following::input[1]")
                            if address_containers:
                                address_container = address_containers[0]
                                address = await page.evaluate('(element) => element.value', address_container)
                            counter += 1

                        customer_containers = await page.xpath("//div[contains(text(), 'Address Description')]/following::input[1]")
                        if customer_containers:
                            customer_container = customer_containers[0]
                            customer_name = await page.evaluate('(element) => element.value', customer_container)

                    # Items Tab
                    order_items = []
                    counter = 0
                    while not order_items and counter < 5:
                        items_tab = await page.xpath("//div[contains(@class, 'mat-tab-label-content') and contains(text(), 'Items')]")
                        if items_tab:
                            await items_tab[0].click()
                

                            extractor = TableDataExtractor(page)
                            order_items_container = await extractor.extract_table_data()

                            for item in order_items_container:
                                order_items.append(item)

                            if not order_items:
                                await dropoff[0].click()
                    
                            counter += 1

                    if not order_items:
                        order_items = [{"SKU": "NULL", "Description": "NULL", "UOM": "NULL", "Special Order": "NULL", "Qty Ordered": "NULL"}]


                    order_dict = {
                        'customer_name': customer_name,
                        'address': address,
                        'order_number': order_number,
                        'status': status,
                        'order_items': order_items
                    }

                    all_orders.append(order_dict)

                    cancel_buttons = await page.xpath("//span[contains(text(), 'Cancel')]")
                    if cancel_buttons:
                        await cancel_buttons[0].click()

        await browser.close()

        # Save the data
        return all_orders


