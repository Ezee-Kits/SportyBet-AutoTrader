# pyppeteer_version_of_sportybot.py
import os
import time
import asyncio
import math
from datetime import datetime
from difflib import SequenceMatcher as ss

import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

from pyppeteer import launch

# Local imports (same as your original)
from func import main_date, save_daily_csv2, saving_files_no_data
from Main_Calc import cal

# ---- Configs ----
browser_delay_time = 6000000
percent = 57

# CSV files path computation same as original
csv_files_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'CSV FILES/{str(main_date())} Files')
save_dir = save_daily_csv2(main_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'CSV FILES'),
                           second_dir_path_name=str(main_date()) + ' Main_Files')
save_path = f'{save_dir}/Data.csv'

# Helper: generate preferred times (keeps your original behaviour)
def generate_preferred_times(current_time):
    try:
        time_obj = datetime.strptime(current_time, "%H:%M")  # Convert string to datetime
        preferred_times = [
            time_obj.strftime("%H:%M")  # EXACT TIME
        ]
        return preferred_times
    except ValueError:
        print("Invalid time format! Use HH:MM")
        return []

def sort_by_time(df, current_time):
    preferred_times = generate_preferred_times(current_time)
    df = df[df['TIME'].isin(preferred_times)]
    df = df.sort_values(by='TIME').reset_index(drop=True)
    return df

# Read CSVs (same as original)
acc_df = pd.read_csv(f'{csv_files_path}/accumulator.csv')
bcl_df = pd.read_csv(f'{csv_files_path}/betclan.csv')
fst_df = pd.read_csv(f'{csv_files_path}/footballsupertips.csv')
frb_df = pd.read_csv(f'{csv_files_path}/forbet.csv')
pre_df = pd.read_csv(f'{csv_files_path}/prematips.csv')
sta_df = pd.read_csv(f'{csv_files_path}/statarea.csv')

# ---- Pyppeteer helpers ----
async def xpath_text(page, xpath, timeout=browser_delay_time):
    """
    Wait for the XPath element then return its textContent (stripped).
    """
    handle = await page.waitForXPath(xpath, timeout=timeout)
    txt = await page.evaluate('(el) => el.textContent', handle)
    return txt.strip() if isinstance(txt, str) else txt

async def xpath_element(page, xpath, timeout=browser_delay_time):
    """
    Wait for an XPath and return the element handle.
    """
    return await page.waitForXPath(xpath, timeout=timeout)

async def click_xpath(page, xpath, timeout=browser_delay_time, scroll_into_view=True, force_sleep=0.5):
    """
    Wait for an XPath, scroll it into view, then click it.
    """
    el = await page.waitForXPath(xpath, timeout=timeout)
    if scroll_into_view:
        await page.evaluate('(el) => el.scrollIntoView({ behavior: "smooth", block: "center" })', el)
        await asyncio.sleep(0.3)
    await el.click()
    if force_sleep:
        await asyncio.sleep(force_sleep)

# place_bet uses page — we will pass page as an argument
async def place_bet(page, edge_amt):
    """
    Fill stake input and place bet using pyppeteer. This is a port of your original logic.
    """
    await asyncio.sleep(1)
    # scroll input into view and set value
    # input selector used in original: 'input.m-input.fs-exclude'
    input_sel = 'input.m-input.fs-exclude'
    # Use js to find and fill input (safer across pyppeteer versions)
    await page.evaluate(f'''
        () => {{
            const el = document.querySelector("{input_sel}");
            if (el) {{
                el.scrollIntoView({{ behavior: "smooth", block: "center" }});
                el.value = "{edge_amt}";
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}
        }}
    ''')
    await asyncio.sleep(1.2)

    # Scroll to place bet button and click
    place_btn_query = 'span[data-cms-key="place_bet"][data-cms-page="component_betslip"]'
    await page.evaluate(f'''
        () => {{
            const el = Array.from(document.querySelectorAll('{place_btn_query}'))
                .find(el => el.textContent && el.textContent.includes("Place Bet"));
            if (el) el.scrollIntoView({{ behavior: "smooth", block: "center" }});
        }}
    ''')
    await asyncio.sleep(0.6)

    # Click the button by evaluating and clicking
    await page.evaluate(f'''
        () => {{
            const el = Array.from(document.querySelectorAll('{place_btn_query}'))
                .find(el => el.textContent && el.textContent.includes("Place Bet"));
            if (el) el.click();
        }}
    ''')
    await asyncio.sleep(1)

    # Click Confirm
    await page.evaluate('''() => {
        const btn = Array.from(document.querySelectorAll('button.af-button.af-button--primary'))
            .find(b => b.textContent && b.textContent.includes("Confirm"));
        if (btn) btn.click();
    }''')
    await asyncio.sleep(2)

    # Click OK dialog if present
    await page.evaluate('''() => {
        const ok = Array.from(document.querySelectorAll('button'))
            .find(b => b.textContent && b.textContent.trim() === "OK");
        if (ok) ok.click();
    }''')
    await asyncio.sleep(1.5)

    # Ensure dialogs are dismissed if any show up
    try:
        page.on('dialog', lambda dialog: asyncio.ensure_future(dialog.dismiss()))
    except Exception:
        # older pyppeteer versions might behave differently; ignore if not supported
        pass

# ---- Main async flow ----
async def main():
    # Use your Chrome installation path and profile dir
    chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    user_data = r'C:\Users\USER\PlaywrightChromeProfile'  # same as your Playwright profile

    # Build args to use persistent profile
    launch_args = [
        f'--user-data-dir={user_data}',
        '--start-maximized',
        '--no-sandbox',
        '--disable-setuid-sandbox'
    ]

    browser = None
    try:
        browser = await launch(executablePath=chrome_path, headless=False, args=launch_args,
                               handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False)
        page = await browser.newPage()
        # maximize viewport similar to no_viewport=True
        await page.setViewport({'width': 1366, 'height': 768})

        url = 'https://www.sportybet.com/ng/sport/football/today'
        await page.goto(url, timeout=browser_delay_time)
        await asyncio.sleep(2)

        # Outer loops preserved: fir_match ranges and sec_match ranges as original
        for fir_match in range(7, 8):
            error_list = []
            for sec_match in range(2, 10):
                print(f'\n CURRENTLY ON SPORTY NUMBER >>>> {fir_match} ON {sec_match}\n')
                # Wait for some main container via XPath (equivalent of your original wait_for_selector)
                await page.waitForXPath('//*[@id="importMatch"]/div[2]/div/div[4]/div[2]', timeout=browser_delay_time)
                await asyncio.sleep(2)

                xpath_target = f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]'
                # Scroll that target into view
                try:
                    el = await page.waitForXPath(xpath_target, timeout=browser_delay_time)
                    await page.evaluate('(el) => el.scrollIntoView({ behavior: "smooth", block: "center" })', el)
                except Exception as e:
                    print(f"Error scrolling to target xpath {xpath_target}: {e}")
                    continue

                await asyncio.sleep(2)

                # Click a nested element (matches your original intent)
                try:
                    click_xpath_1 = f'//*[@id="importMatch"]/div[{fir_match}]/div/div[3]/div[1]'
                    await click_xpath(page, click_xpath_1, timeout=browser_delay_time, scroll_into_view=True, force_sleep=1.2)
                except Exception as e:
                    print(f'Error clicking inner element: {e}')

                await asyncio.sleep(1.5)
                # Scroll again to the match block
                try:
                    el2 = await page.waitForXPath(xpath_target, timeout=browser_delay_time)
                    await page.evaluate('(el) => el.scrollIntoView({ behavior: "smooth", block: "center" })', el2)
                except Exception:
                    pass

                # Extraction using XPath (port of your original lines)
                try:
                    spt_date_raw = await xpath_text(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[1]/div[1]')
                    # original: datetime.strptime(f"2025/{spt_date}", "%Y/%d/%m").strftime("%Y-%m-%d")
                    # their format expects day/month - keep same logic
                    spt_date = datetime.strptime(f"2025/{spt_date_raw}", "%Y/%d/%m").strftime("%Y-%m-%d")
                except Exception as e:
                    print(f"Error extracting date: {e}")
                    spt_date = ''

                try:
                    spt_time = await xpath_text(page,
                                               f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[1]/div/div[1]/div[1]')
                    spt_time = spt_time.strip()
                except Exception as e:
                    print(f"Error extracting time: {e}")
                    spt_time = ''

                try:
                    spt_home_team = await xpath_text(page,
                                                     f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[1]/div/div[2]/div[1]')
                except Exception as e:
                    spt_home_team = ''
                    print(f"Error home team extraction: {e}")

                try:
                    spt_away_team = await xpath_text(page,
                                                     f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[1]/div/div[2]/div[2]')
                except Exception as e:
                    spt_away_team = ''
                    print(f"Error away team extraction: {e}")

                print(spt_date, spt_time, spt_home_team, spt_away_team)

                # Now perform your DataFrame time-sorting and matching logic (same as original)
                current_time = spt_time
                # Protect against empty current_time
                if current_time:
                    try:
                        acc_sorted = sort_by_time(acc_df.copy(), current_time)
                        bcl_sorted = sort_by_time(bcl_df.copy(), current_time)
                        fst_sorted = sort_by_time(fst_df.copy(), current_time)
                        frb_sorted = sort_by_time(frb_df.copy(), current_time)
                        pre_sorted = sort_by_time(pre_df.copy(), current_time)
                        sta_sorted = sort_by_time(sta_df.copy(), current_time)
                    except Exception as e:
                        print(f"Error sorting DFs by time: {e}")
                        # fall back to unsorted copies to avoid crash
                        acc_sorted = acc_df.copy()
                        bcl_sorted = bcl_df.copy()
                        fst_sorted = fst_df.copy()
                        frb_sorted = frb_df.copy()
                        pre_sorted = pre_df.copy()
                        sta_sorted = sta_df.copy()
                else:
                    acc_sorted = acc_df.copy()
                    bcl_sorted = bcl_df.copy()
                    fst_sorted = fst_df.copy()
                    frb_sorted = frb_df.copy()
                    pre_sorted = pre_df.copy()
                    sta_sorted = sta_df.copy()

                all_df_list = [acc_sorted, bcl_sorted, fst_sorted, pre_sorted, sta_sorted]
                print('\n\n22222222222222222222222222222222222222222222222222222222222222222222222222222')

                # Your matching loop over frb_df
                for x in range(len(frb_sorted['HOME TEAM'])):
                    new_df = pd.DataFrame(columns=frb_sorted.columns)
                    new_df = pd.concat([new_df, frb_sorted.iloc[[x]]], ignore_index=True)
                    print('\n')
                    print(f'=====================================  NUMBER : {x}  ========================================')
                    print(f' TIME : {frb_sorted["TIME"].iloc[x]} & HOME TEAM : {frb_sorted["HOME TEAM"].iloc[x]}  &  AWAY TEAM : {frb_sorted["AWAY TEAM"].iloc[x]}')

                    # iterate each external source df
                    for iter_tar in all_df_list:
                        for y in range(len(iter_tar['HOME TEAM'])):
                            try:
                                if frb_sorted['DATE'].iloc[x] == iter_tar['DATE'].iloc[y]:
                                    time1_str = frb_sorted['TIME'].iloc[x]
                                    time2_str = iter_tar['TIME'].iloc[y]
                                    time1 = datetime.strptime(time1_str, "%H:%M")
                                    time2 = datetime.strptime(time2_str, "%H:%M")
                                    time3 = datetime.strptime(spt_time, "%H:%M") if spt_time else time1
                                    time_diff = abs((time1 - time2).total_seconds()) / 60
                                    time_diff2 = abs((time1 - time3).total_seconds()) / 60

                                    if time_diff <= 60 and time_diff2 <= 60:
                                        home_ratio = ss(a=frb_sorted['HOME TEAM'].iloc[x].lower(), b=iter_tar['HOME TEAM'].iloc[y].lower()).ratio() * 100
                                        away_ratio = ss(a=frb_sorted['AWAY TEAM'].iloc[x].lower(), b=iter_tar['AWAY TEAM'].iloc[y].lower()).ratio() * 100
                                        if home_ratio >= percent and away_ratio >= percent:
                                            new_row = iter_tar.iloc[[y]].copy()
                                            new_row.reset_index(drop=True, inplace=True)
                                            new_df = pd.concat([new_df, new_row], ignore_index=True)
                                            break  # Stop searching once a match is found
                            except Exception as e:
                                # protect inner loop from any unexpected errors
                                print(f"Inner matching error: {e}")
                                continue

                # Done iterating frb rows for this particular page region
                # Continue to next sec_match
                await asyncio.sleep(0.2)

        # end for sec_match
        # You may want to break or continue outer loops per your logic
        # time.sleep or asyncio.sleep is fine for pacing between outer iterations
        await asyncio.sleep(1)

    # End for fir_match

    # Any post-processing (merging DFs, saving CSVs) should go here (mirror original logic)
    # Example to merge (you had similar logic further down in original code)
    try:
        df1 = pd.DataFrame(frb_df)
        df2 = pd.DataFrame(ovrund_data) if 'ovrund_data' in globals() else pd.DataFrame()  # placeholder
    except Exception:
        pass

    # Keep browser open until finished - but we will close in finally
    print("Script run completed.")

    # close page if still open
    try:
        await page.close()
    except Exception:
        pass

    # close browser - will also be handled in finally
    try:
        await browser.close()
    except Exception:
        pass

finally:
    # Ensure browser is closed if an exception bubbles up
    try:
        if browser:
            await browser.close()
    except Exception:
        pass

# Run the async main
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
