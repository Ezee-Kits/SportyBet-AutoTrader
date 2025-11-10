from func import main_date,save_daily_csv2
from difflib import SequenceMatcher as ss
from datetime import datetime, timedelta
from datetime import datetime
from pyppeteer import launch
from Main_Calc import cal
import os,math,time
import asyncio
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore',category=pd.errors.PerformanceWarning)


browser_delay_time=60000




async def click_center(page, xpath: str, delay: float = 0.5):
    try:
        # 1️⃣ Wait for element to appear (XPath version)
        await page.waitForXPath(xpath, {'visible': True, 'timeout': 10000})

        # 2️⃣ Get the element handle
        elements = await page.xpath(xpath)
        if not elements:
            print(f"[WARNING] Element not found: {xpath}")
            return False
        
        element = elements[0]

        # 3️⃣ Scroll the element into the center of the viewport
        await page.evaluate('''
            (element) => {
                element.scrollIntoView({
                    behavior: "smooth",
                    block: "center",
                    inline: "center"
                });
            }
        ''', element)

        await asyncio.sleep(delay)  # wait for smooth scrolling

        # 4️⃣ Get the element's bounding box
        box = await element.boundingBox()
        if not box:
            print(f"[WARNING] Element '{xpath}' not visible or has no bounding box.")
            return False

        # 5️⃣ Calculate the center coordinates
        x = box['x'] + box['width'] / 2
        y = box['y'] + box['height'] / 2

        # 6️⃣ Perform the click at the center
        await page.mouse.click(x, y)
        print(f"[OK] Clicked center of '{xpath}' at ({x:.2f}, {y:.2f})")

        return True

    except Exception as e:
        print(f"[ERROR] Could not click on '{xpath}': {e}")
        return False





async def main():
    browser = await launch(
        executablePath=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        headless=False  # Set False if you want to see the browser
    )
    page = await browser.newPage()
    url = 'https://www.sportybet.com/ng/sport/football/today'
    await page.goto(url=url,timeout = 0,waitUntil='networkidle2')
    input("Press Enter after logging in and setting up the page...")
    for fir_match in range(2,3): # MAIN LAYER (2 MINIMUM VALUE)
        sec_match_error_list = []
        for sec_match in range(2,20): # SUB LAYER (2 MINIMUM VALUE)
            print(f'\n CURRENTLY ON SPORTY NUMBER >>>> {fir_match} ON {sec_match}\n')

            # Wait for the first element to appear
            element = await page.waitForXPath('//*[@id="importMatch"]/div[2]/div/div[4]/div[2]')
            await element.getProperty('textContent')
            await asyncio.sleep(2)

            # Scroll element into view
            await page.evaluate(f'''
                el = document.evaluate('//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]',
                document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
            ''')
            # await asyncio.sleep(2)

            # Click on target element
            # click_elem = await page.waitForXPath(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[3]/div[1]',timeout = browser_delay_time)
            # # await click_elem.click()
            # await asyncio.sleep(2)

            # Scroll again to make sure the next section is visible
            await page.evaluate(f'''
                el = document.evaluate('//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]',
                document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
            ''')
#======================================================================================================================================================================================



            # await click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[2]/div[1]')
            # await asyncio.sleep(2)
            print('on over 2.5 now')

#======================================================================================================================================================================================
            
            main_ovr_odd = await page.waitForXPath(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[2]/div[1]')
            main_ovr_odd_text = (await (await main_ovr_odd.getProperty('textContent')).jsonValue()).strip()


            if '2.5' in main_ovr_odd_text:
                print('OVER 2.5 DETECTED, CHECKING FOR EDGE ODDS NOW....')
                try:
                    spt_ovr_odd = await page.waitForXPath(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[2]/div[2]')
                    spt_ovr_odd_text = (await (await spt_ovr_odd.getProperty('textContent')).jsonValue()).strip()
                    
                    print(f'OVER 2.5 EDGE : @ {spt_ovr_odd_text}')
                except Exception as e:
                    print(f"Error fetching over odd: {e}")

                try:
                    spt_und_odd = await page.waitForXPath(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[2]/div[3]')
                    spt_und_odd_text = (await (await spt_und_odd.getProperty('textContent')).jsonValue()).strip()
                    
                    print(f'UNDER 2.5 EDGE :  @ {spt_und_odd_text}')
                except Exception as e:
                    print(f"Error fetching under odd: {e}")

    await asyncio.sleep(10)
    await browser.close()

asyncio.run(main())