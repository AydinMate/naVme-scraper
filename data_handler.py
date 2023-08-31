# from scraper import Scrape
# import asyncio
# import requests

# async def scrape_data(date=None):  # date argument added
#     if date:  # Log the date if provided
#         print(f"Scraping data for date: {date}")

#     url = "https://quotes.toscrape.com/"
#     scraper = Scrape(url)
#     return await scraper.scrape_quotes()

# def send_data_to_endpoint(data):
#     endpoint = "http://localhost:3000/api/get-data"
#     response = requests.post(endpoint, json=data)

#     if response.status_code == 200:
#         return "Data sent", response.status_code
#     else:
#         return "Request failed with status code: ", response.status_code
