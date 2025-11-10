from playwright.sync_api import Playwright,sync_playwright
from func import main_date,save_daily_csv2,saving_files_no_data
from difflib import SequenceMatcher as ss
from datetime import datetime, timedelta
from datetime import datetime
from Main_Calc import cal
import os,math,time
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore',category=pd.errors.PerformanceWarning)


browser_delay_time=6000000

csv_files_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'CSV FILES/{str(main_date())} Files')

save_dir = save_daily_csv2(main_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)),'CSV FILES'),second_dir_path_name=str(main_date())+' Main_Files')
save_path = f'{save_dir}/Data.csv'

def generate_preferred_times(current_time):
    try:
        time_obj = datetime.strptime(current_time, "%H:%M")  # Convert string to datetime
        preferred_times = [  # 1 hour before
            time_obj.strftime("%H:%M") # EXACT TIME
        ]
        return preferred_times
    except ValueError:
        print("Invalid time format! Use HH:MM")
        return []

# Function to sort DataFrame by dynamically generated preferred times
def sort_by_time(df, current_time):
    preferred_times = generate_preferred_times(current_time)  # Get preferred times
    df = df[df['TIME'].isin(preferred_times)]
    df = df.sort_values(by='TIME').reset_index(drop=True)
    return df


        # Read the CSV files
acc_df = pd.read_csv(f'{csv_files_path}/accumulator.csv')
bcl_df = pd.read_csv(f'{csv_files_path}/betclan.csv')
fst_df = pd.read_csv(f'{csv_files_path}/footballsupertips.csv')
frb_df = pd.read_csv(f'{csv_files_path}/forbet.csv')
pre_df = pd.read_csv(f'{csv_files_path}/prematips.csv')
sta_df = pd.read_csv(f'{csv_files_path}/statarea.csv')

percent = 57

def place_bet(edge_amt):
    ## [[[[[ PLACE BET SECTION ]]]]
    time.sleep(5)
    page.eval_on_selector(f'input.m-input.fs-exclude', "el => el.scrollIntoView({ behavior: 'smooth', block: 'center' })")
    input_element = page.wait_for_selector('input.m-input.fs-exclude',timeout=browser_delay_time)

    input_element.fill(str(edge_amt))
    time.sleep(3)
    page.eval_on_selector(f'span[data-cms-key="place_bet"][data-cms-page="component_betslip"]:has-text("Place Bet")', "el => el.scrollIntoView({ behavior: 'smooth', block: 'center' })")
    place_bet_element = page.locator('span[data-cms-key="place_bet"][data-cms-page="component_betslip"]:has-text("Place Bet")')
    place_bet_element.scroll_into_view_if_needed()
    time.sleep(1.3)
    place_bet_element.click(force=True)
    time.sleep(1.5)
    place_bet_element.click(force=True)
    time.sleep(1.5)
    confirm_button = page.locator('button.af-button.af-button--primary:has-text("Confirm")')
    confirm_button.click(force=True)
    time.sleep(3)
    page.eval_on_selector(f"button:has-text('OK')", "el => el.scrollIntoView({ behavior: 'smooth', block: 'center' })")
    ok_button = page.wait_for_selector("button:has-text('OK')", timeout=5000)
    time.sleep(2)
    ok_button.click()
    time.sleep(2)
   
    page.on("dialog", lambda dialog: dialog.dismiss())
    time.sleep(2)



with sync_playwright() as playwright:
    user_data = "C:\\Users\\USER\\PlaywrightChromeProfile"
    context = playwright.chromium.launch_persistent_context(user_data_dir=user_data,channel='chrome',headless=False,args=["--start-maximized"],no_viewport=True)
    page = context.new_page()
    url = 'https://www.sportybet.com/ng/sport/football/today'
    page.goto(url=url,timeout = browser_delay_time)

    for fir_match in range(7,8):
        error_list = []
        # try:
        for sec_match in range(2,10):
            # if len(error_list) >=2:
            #     break
            print(f'\n CURRENTLY ON SPORTY NUMBER >>>> {fir_match} ON {sec_match}\n')
            page.wait_for_selector('//*[@id="importMatch"]/div[2]/div/div[4]/div[2]').text_content()
            time.sleep(5)
            page.eval_on_selector(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]', "el => el.scrollIntoView({ behavior: 'smooth', block: 'center' })")
            time.sleep(2)

            page.wait_for_selector(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[3]/div[1]',timeout=browser_delay_time).click()
            time.sleep(2)
            page.eval_on_selector(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]', "el => el.scrollIntoView({ behavior: 'smooth', block: 'center' })")
            
            spt_date = page.wait_for_selector(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[1]/div[1]').text_content().split()[0]
            spt_date = datetime.strptime(f"2025/{spt_date}", "%Y/%d/%m").strftime("%Y-%m-%d")
            spt_time = page.wait_for_selector(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[1]/div/div[1]/div[1]').text_content().strip()
            spt_home_team = page.wait_for_selector(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[1]/div/div[2]/div[1]').text_content().strip()
            spt_home_team_tag = page.wait_for_selector(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[1]/div/div[2]/div[1]')
            spt_away_team = page.wait_for_selector(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[1]/div/div[2]/div[2]').text_content().strip()
            print(spt_date,spt_time,spt_home_team,spt_away_team)
            

            current_time = spt_time
            acc_df = sort_by_time(acc_df, current_time)
            bcl_df = sort_by_time(bcl_df, current_time)
            fst_df = sort_by_time(fst_df, current_time)
            frb_df = sort_by_time(frb_df, current_time)
            pre_df = sort_by_time(pre_df, current_time)
            sta_df = sort_by_time(sta_df, current_time)
            
            all_df = [acc_df,bcl_df,fst_df,pre_df,sta_df]
            print('\n\n22222222222222222222222222222222222222222222222222222222222222222222222222222')

            for x in range(len(frb_df['HOME TEAM'])):
                new_df = pd.DataFrame(columns=frb_df.columns)
                new_df = pd.concat([new_df, frb_df.iloc[[x]]], ignore_index=True)
                print('\n')
                print(f'=====================================  NUMBER : {x}  ========================================')
                print(f' TIME : {frb_df["TIME"][x]} & HOME TEAM : {frb_df["HOME TEAM"][x]}  &  AWAY TEAM : {frb_df["AWAY TEAM"][x]}')
                for iter_tar in all_df:
                    for y in range(len(iter_tar['HOME TEAM'])):
                        if frb_df['DATE'][x] == iter_tar['DATE'][y]:
                            # Extract time strings directly
                            time1_str = frb_df['TIME'][x]
                            time2_str = iter_tar['TIME'][y]
                            time1 = datetime.strptime(time1_str, "%H:%M")
                            time2 = datetime.strptime(time2_str, "%H:%M")
                            time3 = datetime.strptime(spt_time, "%H:%M")
                            time_diff = abs((time1 - time2).total_seconds()) / 60
                            time_diff2 = abs((time1 - time3).total_seconds()) / 60
                            if time_diff <= 60 and time_diff2 <= 60 and \
                                ss(a=frb_df['HOME TEAM'][x].lower(), b=iter_tar['HOME TEAM'][y].lower()).ratio() * 100 >= percent and \
                                ss(a=frb_df['AWAY TEAM'][x].lower(), b=iter_tar['AWAY TEAM'][y].lower()).ratio() * 100 >= percent:
                                new_row = iter_tar.iloc[[y]].copy()
                                new_row.reset_index(drop=True, inplace=True)  # Prevent incorrect indexing
                                new_df = pd.concat([new_df, new_row], ignore_index=True)
                                break  # Stop searching once a match is found