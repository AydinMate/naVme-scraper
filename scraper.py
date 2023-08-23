
from pyppeteer import launch

class Scrape:
    def __init__(self, url):
        self.url = url
        self.viewport_options = {
            "width": 1080,
            "height": 1024,
            "deviceScaleFactor": 1.0,
            "isMobile": False,
            "hasTouch": False,
            "isLandscape": False
        }

    async def scrape_quotes(self):
        browser = await launch(headless=True)
        page = await browser.newPage()
        await page.goto(self.url)
        await page.setViewport(viewport=self.viewport_options)

        await page.waitForSelector('.quote')
        quote_elements = await page.querySelectorAll('.quote')

        quote_data_array = []
        for quote_element in quote_elements:
            text_element = await quote_element.querySelector('.text')
            text = (await page.evaluate('(text_element) => text_element.textContent', text_element)).strip()

            author_element = await quote_element.querySelector('.author')
            author = (await page.evaluate('(author_element) => author_element.textContent', author_element)).strip()

            text_data = {
                'author': author,
                'text': text,
            }

            quote_data_array.append(text_data)

        await browser.close()
        return quote_data_array


