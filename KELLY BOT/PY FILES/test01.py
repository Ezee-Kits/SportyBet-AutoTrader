import os,math,time
import pandas as pd
from difflib import SequenceMatcher as ss
from datetime import datetime, timedelta
from func import main_date

csv_files_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'CSV FILES/{str(main_date())} Files')


acc_df = pd.read_csv(f'{csv_files_path}/accumulator.csv')
bcl_df = pd.read_csv(f'{csv_files_path}/betclan.csv')
fst_df = pd.read_csv(f'{csv_files_path}/footballsupertips.csv')
frb_df = pd.read_csv(f'{csv_files_path}/forebet.csv')
pre_df = pd.read_csv(f'{csv_files_path}/prematips.csv')
sta_df = pd.read_csv(f'{csv_files_path}/statarea.csv')

percent = 57



def sort_by_time(df, current_time):
    try:
        # Convert the string time to datetime object
        time_obj = datetime.strptime(current_time, "%H:%M")

        # Define the time range (1 hour before and 1 hour after)
        start_time = time_obj - timedelta(hours=1)
        end_time = time_obj + timedelta(hours=1)

        # Convert 'TIME' column to datetime objects for comparison
        df['TIME_DT'] = pd.to_datetime(df['TIME'], format="%H:%M", errors='coerce')

        # Keep only rows within the ±1-hour window
        filtered_df = df[(df['TIME_DT'] >= start_time) & (df['TIME_DT'] <= end_time)]

        # Sort and reset index
        filtered_df = filtered_df.sort_values(by='TIME_DT').reset_index(drop=True)

        # Drop helper column
        filtered_df = filtered_df.drop(columns=['TIME_DT'])

        return filtered_df

    except Exception as e:
        print(f"Error sorting by time: {e}")
        return df



def main():
    global acc_df, bcl_df, fst_df, frb_df, pre_df, sta_df
    # Example usage
    # current_time = "15:30"  # This would be dynamically set in a real scenario
    for x in range(5):
        for y in range(5):
            print(f'{x} - {y}')
            spt_time = '20:00'
            current_time = spt_time

            acc_df = sort_by_time(acc_df, current_time)
            bcl_df = sort_by_time(bcl_df, current_time)
            fst_df = sort_by_time(fst_df, current_time)
            frb_df = sort_by_time(frb_df, current_time)
            pre_df = sort_by_time(pre_df, current_time)
            sta_df = sort_by_time(sta_df, current_time)

            all_df = [acc_df,bcl_df,fst_df,pre_df,sta_df]

            print('\n\n22222222222222222222222222222222222222222222222222222222222222222222222222222')

            for frb_cont in range(len(frb_df['HOME TEAM'])):
                new_df = pd.DataFrame(columns=frb_df.columns)
                new_df = pd.concat([new_df, frb_df.iloc[[frb_cont]]], ignore_index=True)
                print('\n')
                print(f'=====================================  NUMBER : {frb_cont}  ========================================')
                print(f' TIME : {frb_df["TIME"][frb_cont]} & HOME TEAM : {frb_df["HOME TEAM"][frb_cont]}  &  AWAY TEAM : {frb_df["AWAY TEAM"][frb_cont]}')
                for iter_tar in all_df:
                    for y in range(len(iter_tar['HOME TEAM'])):
                        # if frb_df['DATE'][frb_cont] == iter_tar['DATE'][y]: #DONT FEEL LIKE USING THE DATE FOR
                        # Extract time strings directly
                        time1_str = frb_df['TIME'][frb_cont]
                        time2_str = iter_tar['TIME'][y]
                        time1 = datetime.strptime(time1_str, "%H:%M")
                        time2 = datetime.strptime(time2_str, "%H:%M")
                        time3 = datetime.strptime(spt_time, "%H:%M")
                        time_diff = abs((time1 - time2).total_seconds()) / 120
                        time_diff2 = abs((time1 - time3).total_seconds()) / 120
                        if time_diff <= 120 and time_diff2 <= 120 and \
                            ss(a=frb_df['HOME TEAM'][frb_cont].lower(), b=iter_tar['HOME TEAM'][y].lower()).ratio() * 100 >= percent and \
                            ss(a=frb_df['AWAY TEAM'][frb_cont].lower(), b=iter_tar['AWAY TEAM'][y].lower()).ratio() * 100 >= percent:
                            new_row = iter_tar.iloc[[y]].copy()
                            new_row.reset_index(drop=True, inplace=True)  # Prevent incorrect indexing
                            new_df = pd.concat([new_df, new_row], ignore_index=True)
                            break  # Stop searching once a match is found

                
                print(new_df)
                # frb_time = new_df['TIME'][0]
                # frb_home_team = new_df['HOME TEAM'][0]
                # frb_away_team = new_df['AWAY TEAM'][0]
                # frb_home_per = round(new_df['HOME PER'].mean(), 2)
                # frb_draw_per = round(new_df['DRAW PER'].mean(), 2)
                # frb_away_per = round(new_df['AWAY PER'].mean(), 2)
                # frb_ovr25_per = round(new_df['OVER 2.5'].mean(), 2)
                # frb_und25_per = round(new_df['UNDER 2.5'].mean(), 2)
                # frb_bts_per = round(new_df['BTS'].mean(), 2)
                # frb_ots_per = round(new_df['OTS'].mean(), 2)

                # print(frb_time, frb_home_team, frb_away_team, frb_home_per, frb_draw_per, frb_away_per, frb_ovr25_per, frb_und25_per, frb_bts_per, frb_ots_per)
                # break

main()