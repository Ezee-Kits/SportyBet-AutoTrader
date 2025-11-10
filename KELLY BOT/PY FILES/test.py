# import time

# match_date =time.localtime() 

# # f'{match_date[0]}-{match_date[1]:02}-{match_date[2]}'
# print(f'{match_date[0]}-{match_date[1]}-{match_date[2]}')


# a = [4,6,8,9,0,23,45,12,34,16]
# for x in range(1,len(a),3):
#     print(a[x] )


# for i in range(20):  # scroll 20 times --- IGNORE ---
#     await page.evaluate('window.scrollBy(0, window.innerHeight)') # (+ down, - up)
#     await asyncio.sleep(1)

# a = '18/10/2025 15:00'
# print(a.split(' ')[1])



# # Save to file
# with open("forebet_1x2.html", "w", encoding="utf-8") as f:
#     f.write(html_content)

# # Load the saved HTML file
# with open("forebet_1x2.html", "r", encoding="utf-8") as f:
#     html_content = f.read()

# a =[[2],[4],[9]]
# print(len(a))
# print(7200/60)

# from func import main_date
# print(main_date())


# a = 9
# if a> 7:
#     print('yes')
# print(a)



# from func import requests_init,saving_files,drop_duplicate

# drop_duplicate(path='PY FILES/tic_tac_toe_training_weighted.csv')



# from func import main_date,save_daily_csv2,saving_files
# import os
# import pandas as pd

# save_dir = save_daily_csv2(main_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)),'CSV FILES'),second_dir_path_name=str(main_date())+' Main_Files')
# save_path = f'{save_dir}/Data.csv'

# pp_data = {'INFO':[]}

# # print(spt_date, spt_time, spt_home_team, spt_away_team)
# pp_data['INFO'].append(f'spt_date-spt_time-spt_home_team-spt_away_team')


# pp_data_df = pd.read_csv(save_path) #['INFO'].to_list()
# print(len(pp_data_df))

# if 'spt_date-spt_time-spt_home_team-spt_away_team' not in pp_data_df:
#     saving_files(data=pp_data,path=save_path)
#     print('rannnn')
#     print(pp_data_df)



# for x in range(5):
#     print('x:',x)
#     for y in range(15):
#         print('y:',y)
#         if y==8:
#             break
#         print('obi is a boy',y)



# a = 8
# for x in range(3):
#     try:
#         print(a+b)
#     except:
#         print('error occured')
#         try:
#             print(c)
#         except:
#             print('error occured in c')
#             break



# from func import main_date,save_daily_csv2
# import os,math,time
# import asyncio
# import pandas as pd

# save_dir = save_daily_csv2(main_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)),'CSV FILES'),second_dir_path_name=str(main_date())+' Main_Files')
# save_path = f'{save_dir}/Data.csv'


# pp_data = {'INFO':[]}
# pp_target = f'spt_date-spt_time-spt_home_team-spt_away_team'
# pp_data['INFO'].append(pp_target)

# try:
#     pp_data_df = pd.read_csv(save_path)['INFO'].to_list()
# except:
#     pp_data_df = pd.DataFrame({'INFO':['starting']})['INFO'].to_list()

# print(pp_data_df)









# def sort_by_time(df, current_time):
#     try:
#         # Convert the string time to datetime object
#         time_obj = datetime.strptime(current_time, "%H:%M")

#         # Define the time range (1 hour before and 1 hour after)
#         start_time = time_obj - timedelta(hours=1)
#         end_time = time_obj + timedelta(hours=1)

#         # Convert 'TIME' column to datetime objects for comparison
#         df['TIME_DT'] = pd.to_datetime(df['TIME'], format="%H:%M", errors='coerce')

#         # Keep only rows within the ±1-hour window
#         filtered_df = df[(df['TIME_DT'] >= start_time) & (df['TIME_DT'] <= end_time)]

#         # Sort and reset index
#         filtered_df = filtered_df.sort_values(by='TIME_DT').reset_index(drop=True)

#         # Drop helper column
#         filtered_df = filtered_df.drop(columns=['TIME_DT'])

#         return filtered_df
#     except Exception as e:
#         print(f"Error sorting by time: {e}")
#         return df



# from func import main_date,save_daily_csv2
# import os,math,time
# import asyncio
# import pandas as pd
# from difflib import SequenceMatcher as ss



# percent=57
# csv_files_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'CSV FILES/{str(main_date())} Files')

# def sort_by_name(df, spt_home_team, spt_away_team, percent):
#     try:
#         # Calculate similarity for home team
#         df['HOME_SIMILARITY'] = df['HOME TEAM'].apply(
#             lambda x: ss(None, str(x).lower(), str(spt_home_team).lower()).ratio() * 100
#         )

#         # Calculate similarity for away team
#         df['AWAY_SIMILARITY'] = df['AWAY TEAM'].apply(
#             lambda x: ss(None, str(x).lower(), str(spt_away_team).lower()).ratio() * 100
#         )

#         # Keep only rows where BOTH home & away similarity >= threshold
#         filtered_df = df[
#             (df['HOME_SIMILARITY'] >= percent) &
#             (df['AWAY_SIMILARITY'] >= percent)
#         ].copy()

#         # Sort by total similarity (combined)
#         filtered_df['TOTAL_SIMILARITY'] = (
#             filtered_df['HOME_SIMILARITY'] + filtered_df['AWAY_SIMILARITY']
#         ) / 2

#         filtered_df = filtered_df.sort_values(by='TOTAL_SIMILARITY', ascending=False).reset_index(drop=True)

#         # Drop helper columns
#         filtered_df = filtered_df.drop(columns=['HOME_SIMILARITY', 'AWAY_SIMILARITY', 'TOTAL_SIMILARITY'])

#         return filtered_df

#     except Exception as e:
#         print(f"Error sorting by team similarity: {e}")
#         return df



# spt_home_team = 'Skeid'
# spt_away_team = 'Raufoss'

# acc_df_f = pd.read_csv(f'{csv_files_path}/accumulator.csv')
# acc_df = sort_by_name(acc_df_f, spt_home_team, spt_away_team, percent)

# print(acc_df)













a = 8

if a ==9:
    print('1')
elif a:
    print('2')
    

# from pyppeteer import launch
# import asyncio


# async def main():
#     global acc_df, bcl_df, fst_df, frb_df, pre_df, sta_df
#     SN_page = [] #SEARCHED NEXT PAGE
#     browser = await launch(
#         executablePath=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
#         headless=False  # Set False if you want to see the browser
#     )

    
#     page = await browser.newPage()
#     url = 'https://www.sportybet.com/ng/sport/football/today'
#     await page.goto(url=url,timeout = 0,waitUntil='networkidle2')

#     # Click the element using XPath
#     xpath = '//*[@id="importMatch"]/div[2]/div/div[4]/div[5]/div[2]/div[2]/div[1]'
    
#     elements = await page.xpath(xpath)
#     if elements:
#         await elements[0].click()
#         await asyncio.sleep(1)  # Give time for dropdown animation
#     else:
#         print("❌ Dropdown trigger not found")
#         await browser.close()
#         return


#     # Wait for dropdown container (more reliable selector)
#     await page.waitForSelector('.af-select-list-open', {'visible': True, 'timeout': 60000})
#     # Click the "2.5" option
#     await page.evaluate('''() => {
#         const options = document.querySelectorAll('.af-select-list-open .af-select-item');
#         for (let opt of options) {
#             if (opt.textContent.trim() === '2.5') {
#                 opt.click();
#                 break;
#             }
#         }
#     }''')

#     print('Clicked 2.5 option')
#     await asyncio.sleep(30)


#     await browser.close()

# asyncio.run(main())






# from datetime import datetime, timedelta
# from difflib import SequenceMatcher as ss
# import os
# from func import main_date,save_daily_csv2
# import os,math,time
# import asyncio
# import pandas as pd
# from difflib import SequenceMatcher as ss


# percent=57
# csv_files_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'CSV FILES/{str(main_date())} Files')



# def sort_by_name_and_time_exact(df, spt_home_team, spt_away_team, spt_time, percent):
#     try:
#         # Step 1: Calculate similarity for home team
#         df['HOME_SIMILARITY'] = df['HOME TEAM'].apply(
#             lambda x: ss(None, str(x).lower(), str(spt_home_team).lower()).ratio() * 100
#         )

#         # Step 2: Calculate similarity for away team
#         df['AWAY_SIMILARITY'] = df['AWAY TEAM'].apply(
#             lambda x: ss(None, str(x).lower(), str(spt_away_team).lower()).ratio() * 100
#         )

#         # Step 3: Keep rows where both similarities >= threshold
#         filtered_df = df[
#             (df['HOME_SIMILARITY'] >= percent) &
#             (df['AWAY_SIMILARITY'] >= percent)
#         ].copy()

#         if filtered_df.empty:
#             return filtered_df  # nothing matches, return empty

#         # Step 4: Sort by combined similarity
#         filtered_df['TOTAL_SIMILARITY'] = (
#             filtered_df['HOME_SIMILARITY'] + filtered_df['AWAY_SIMILARITY']
#         ) / 2
#         filtered_df = filtered_df.sort_values(by='TOTAL_SIMILARITY', ascending=False).reset_index(drop=True)

#         # Step 5: Filter by exact times (1 hour before, same hour, and 1 hour after)
#         spt_time_dt = datetime.strptime(spt_time, "%H:%M")

#         valid_times = {
#             (spt_time_dt - timedelta(hours=1)).strftime("%H:%M"),  # 1 hour before
#             spt_time_dt.strftime("%H:%M"),                         # exact time
#             (spt_time_dt + timedelta(hours=1)).strftime("%H:%M")   # 1 hour after
#         }

#         filtered_df = filtered_df[filtered_df['TIME'].isin(valid_times)].reset_index(drop=True)

#         # Step 6: Drop helper columns
#         filtered_df = filtered_df.drop(columns=['HOME_SIMILARITY', 'AWAY_SIMILARITY', 'TOTAL_SIMILARITY'])

#         return filtered_df

#     except Exception as e:
#         print(f"Error sorting by team similarity and time: {e}")
#         return df



# spt_home_team = 'Midtjylland'
# spt_away_team = 'Celtic'
# spt_time = '18:45'  # for example

# acc_df_f = pd.read_csv(f'{csv_files_path}/accumulator.csv')
# bcl_df_f = pd.read_csv(f'{csv_files_path}/betclan.csv')
# fst_df_f = pd.read_csv(f'{csv_files_path}/footballsupertips.csv')
# frb_df_f = pd.read_csv(f'{csv_files_path}/forebet.csv')
# pre_df_f = pd.read_csv(f'{csv_files_path}/prematips.csv')
# sta_df_f = pd.read_csv(f'{csv_files_path}/statarea.csv')

# acc_df = sort_by_name_and_time_exact(acc_df_f, spt_home_team, spt_away_team, spt_time, percent)
# bcl_df = sort_by_name_and_time_exact(bcl_df_f, spt_home_team, spt_away_team, spt_time, percent)
# fst_df = sort_by_name_and_time_exact(fst_df_f, spt_home_team, spt_away_team, spt_time, percent)
# frb_df = sort_by_name_and_time_exact(frb_df_f, spt_home_team, spt_away_team, spt_time, percent)
# pre_df = sort_by_name_and_time_exact(pre_df_f, spt_home_team, spt_away_team, spt_time, percent)
# sta_df = sort_by_name_and_time_exact(sta_df_f, spt_home_team, spt_away_team, spt_time, percent)


# # First, create a list of your filtered dataframes
# all_df_list = [acc_df, bcl_df, fst_df, frb_df, pre_df, sta_df]

# # Concatenate them into a single dataframe
# combined_df = pd.concat(all_df_list, ignore_index=True)

# # Optional: sort combined_df by some column, e.g., 'TIME' or 'TOTAL_SIMILARITY' if still present
# # combined_df = combined_df.sort_values(by='TIME').reset_index(drop=True)

# print(combined_df)

# print(len(combined_df))



















# import tkinter as tk
# from tkinter import simpledialog

# def start_btn():
#     class StartDialog(simpledialog.Dialog):
#         def body(self, master):
#             self.geometry("250x120")
#             self.title("Automation")
#             # Label text
#             tk.Label(master, text="Click Start to begin automation", font=("Arial", 12)).pack(pady=20)
#             return None  # No input field needed

#         def buttonbox(self):
#             box = tk.Frame(self)
#             # Start button
#             tk.Button(box, text="Start", width=10, command=self.ok).pack(pady=10)
#             box.pack()

#     # Main root
#     root = tk.Tk()
#     root.withdraw()  # hide main window

#     dlg = StartDialog(root)  # show dialog

#     print("Automation started!")  # runs after Start clicked
#     root.destroy()


