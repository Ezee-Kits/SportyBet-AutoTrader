import asyncio
from pyppeteer import launch

async def main():
    browser = await launch({
        'executablePath': '/data/data/com.termux/files/usr/lib/chromium/chrome',
        'args': [
            '--no-sandbox',
            '--disable-gpu',
            '--disable-dev-shm-usage',
            '--disable-software-rasterizer',
            '--disable-setuid-sandbox',
            '--enable-features=UseOzonePlatform',
            '--ozone-platform=x11'
        ],
        'headless': False,
        'userDataDir': '/data/data/com.termux/files/home/BrowserData'
    })
    page = await browser.newPage()
    await page.goto('https://www.sportybet.com')

    input("Press ENTER to stop... ")

    print("Chromium launched successfully and opened Sportybet!")

    await asyncio.sleep(5)
    await browser.close()

asyncio.run(main())