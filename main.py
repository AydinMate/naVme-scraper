from scraper import Scrape
import asyncio

import requests

async def main():
    url = "https://quotes.toscrape.com/"
    scraper = Scrape(url)
    quote_data_array = await scraper.scrape_quotes()
    return quote_data_array

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(main())




endpoint = "http://localhost:3000/api/get-data"


response = requests.post(endpoint, json=data)

if response.status_code == 200:
    print("Data sent")
else:
    print("Request failed with status code:", response.status_code)