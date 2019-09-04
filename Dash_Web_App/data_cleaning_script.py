#import libraries
import pandas as pd
import numpy as np

#import data files
exercise_df = pd.read_csv("original_data/exercise.csv", sep=',', index_col=0)
floors_df = pd.read_csv("original_data/floors_climbed.csv", sep=',', index_col=0)
heart_rate_df = pd.read_csv("original_data/heart_rate.csv", sep=',', index_col=0)
sleep_df = pd.read_csv("original_data/sleep.csv", sep=',', index_col=0)
step_count_df = pd.read_csv("original_data/step_count.csv", sep=',', index_col=0)
summary_df = pd.read_csv("original_data/summary.csv", sep=',', index_col=0)


#######SLEEP DATA
#remove empty columns from SLEEP data
for col in sleep_df.columns:
    description = sleep_df[col].isnull().describe()
    if (description.top == True) and (description.freq == sleep_df[col].isnull().count()):
        del sleep_df[col]


#function for adjusting time
def to_float(x):
    return float(x[1])/100

#adjust time by offset for SLEEP data	
hr_offset = sleep_df['com.samsung.health.sleep.time_offset'].str.split('UTC').apply(to_float)
timeIndex_offset = pd.TimedeltaIndex(hr_offset, unit='h')
sleep_df['local_start_time'] = pd.to_datetime(sleep_df['com.samsung.health.sleep.start_time'], origin='unix', unit='ms') + timeIndex_offset
sleep_df['local_end_time'] = pd.to_datetime(sleep_df['com.samsung.health.sleep.end_time'], origin='unix', unit='ms') + timeIndex_offset


#combine rows that have sleep interuption less than 1 hour
combine = []
combine_dict = {}

def first_iteration(x):
    i = sleep_df.apply(second_iteration, args=(x.name,x.local_start_time,), axis=1)
    return
	
def second_iteration(x, y, start_time):
    if (x.name != y) and (abs(x.local_end_time - start_time) < pd.Timedelta(1, unit='h')) and (y not in combine_dict):
        combine.append((x.name, y))
        combine_dict[x.name] = y
    return
	
sleep_df.sort_values('local_start_time', axis=0, ascending=False).apply(first_iteration, axis=1)

for j,i in combine:
    total_time_1 = abs(sleep_df.loc[i].local_end_time - sleep_df.loc[i].local_start_time)
    total_time_2 = abs(sleep_df.loc[j].local_end_time - sleep_df.loc[j].local_start_time)
    sleep_df.at[i, 'efficiency'] = 100*(total_time_1*sleep_df.loc[i].efficiency/100 + total_time_2*sleep_df.loc[j].efficiency/100)/(total_time_1 + total_time_2 + min(abs(sleep_df.loc[i].local_start_time - sleep_df.loc[j].local_end_time),abs(sleep_df.loc[j].local_start_time - sleep_df.loc[i].local_end_time)))
    sleep_df.at[i, 'local_start_time'] = min(sleep_df.loc[i].local_start_time, sleep_df.loc[j].local_start_time)
    sleep_df.at[i, 'local_end_time'] = max(sleep_df.loc[i].local_end_time, sleep_df.loc[j].local_end_time)
    sleep_df.at[i, 'has_sleep_data'] = max(sleep_df.loc[i].has_sleep_data, sleep_df.loc[j].has_sleep_data)
    sleep_df.at[i, 'quality'] = max(sleep_df.loc[i].quality, sleep_df.loc[j].quality)
    sleep_df.drop(j, axis=0, inplace=True)

#rename columns to shorter names
sleep_df.rename(index=str, columns={"com.samsung.health.sleep.time_offset":"time_offset", "com.samsung.health.sleep.deviceuuid":"deviceuuid"}, inplace=True)

#remove unsed columns from SLEEP data
sleep_df.drop(['com.samsung.health.sleep.datauuid','com.samsung.health.sleep.pkg_name','original_efficiency','original_bed_time','original_wake_up_time','com.samsung.health.sleep.start_time','com.samsung.health.sleep.end_time','com.samsung.health.sleep.update_time','com.samsung.health.sleep.create_time','has_sleep_data'], axis=1, inplace=True)



#######FLOORS DATA
#remove empty columns from FLOORS data
for col in floors_df.columns:
    description = floors_df[col].isnull().describe()
    if (description.top == True) and (description.freq == floors_df[col].isnull().count()):
        del floors_df[col]


#adjust time by offset for FLOORS data
hr_offset = floors_df['time_offset'].str.split('UTC').apply(to_float)
timeIndex_offset = pd.TimedeltaIndex(hr_offset, unit='h')
floors_df['local_start_time'] = pd.to_datetime(floors_df['start_time']) + timeIndex_offset
floors_df['local_end_time'] = pd.to_datetime(floors_df['end_time']) + timeIndex_offset


#remove unsed columns from FLOORS data
floors_df.drop(['pkg_name','datauuid','start_time','end_time','create_time','update_time'], axis=1, inplace=True)



#######HEART_RATE DATA
#remove empty columns from HEART_RATE data
for col in heart_rate_df.columns:
    description = heart_rate_df[col].isnull().describe()
    if (description.top == True) and (description.freq == heart_rate_df[col].isnull().count()):
        del heart_rate_df[col]

		
#adjust time by offset for HEART_RATE data
hr_offset = heart_rate_df['time_offset'].str.split('UTC').apply(to_float)
timeIndex_offset = pd.TimedeltaIndex(hr_offset, unit='h')
heart_rate_df['local_start_time'] = pd.to_datetime(heart_rate_df['start_time']) + timeIndex_offset
heart_rate_df['local_end_time'] = pd.to_datetime(heart_rate_df['end_time']) + timeIndex_offset


#remove unsed columns from HEART_RATE data
heart_rate_df.drop(['pkg_name','datauuid','binning_data','heart_beat_count','create_time','update_time','end_time','start_time'], axis=1, inplace=True)

#remove entries with incorrect timestamp
heart_rate_df = heart_rate_df[heart_rate_df['local_start_time'].dt.year >= 2012]


#######STEP_COUNT DATA
#remove empty columns from STEP_COUNT data
for col in step_count_df.columns:
    description = step_count_df[col].isnull().describe()
    if (description.top == True) and (description.freq == step_count_df[col].isnull().count()):
        del step_count_df[col]

		
#adjust time by offset for STEP_COUNT data
hr_offset = step_count_df['time_offset'].str.split('UTC').apply(to_float)
timeIndex_offset = pd.TimedeltaIndex(hr_offset, unit='h')
step_count_df['local_start_time'] = pd.to_datetime(step_count_df['start_time']) + timeIndex_offset
step_count_df['local_end_time'] = pd.to_datetime(step_count_df['end_time']) + timeIndex_offset


#remove unsed columns from STEP_COUNT data
step_count_df.drop(['pkg_name','datauuid','create_time','update_time','end_time','start_time'], axis=1, inplace=True)



#######EXERCISE DATA
#remove empty columns from EXERCISE data
for col in exercise_df.columns:
    description = exercise_df[col].isnull().describe()
    if (description.top == True) and (description.freq == exercise_df[col].isnull().count()):
        del exercise_df[col]
	
	
#adjust time by offset for EXERCISE data
hr_offset = exercise_df['time_offset'].str.split('UTC').apply(to_float)
timeIndex_offset = pd.TimedeltaIndex(hr_offset, unit='h')
exercise_df['local_start_time'] = pd.to_datetime(exercise_df['start_time']) + timeIndex_offset
exercise_df['local_end_time'] = pd.to_datetime(exercise_df['end_time']) + timeIndex_offset


#remove unsed columns from EXERCISE data
exercise_df.drop(['pkg_name','datauuid','location_data','comment','live_data','create_time','update_time','start_time','end_time'], axis=1, inplace=True)

#remove casual walk entries
exercise_df = exercise_df[(exercise_df['exercise_type'] != 1001) | ((exercise_df['exercise_type'] == 1001) & (exercise_df['mean_speed'] > 1.5) & (exercise_df['distance'] > 900))]
exercise_df['duration'] = exercise_df['duration']/60000

#convert exercise type from int to str
exercise_df['exercise_type'] = exercise_df['exercise_type'].astype(str)
exercise_df['count_type'] = exercise_df['count_type'].astype(str)
exercise_df = exercise_df.replace('0', 'custom')
exercise_df = exercise_df.replace('1001', 'walking')
exercise_df = exercise_df.replace('1002', 'running')
exercise_df = exercise_df.replace('11007', 'cycling')
exercise_df = exercise_df.replace('13001', 'hiking')
exercise_df = exercise_df.replace('14001', 'swimming')
exercise_df = exercise_df.replace('15006', 'elliptical')
exercise_df = exercise_df.replace('30001.0', 'stride')
exercise_df = exercise_df.replace('30004.0', 'repetition')



#######SUMMARY DATA
#remove empty columns from SUMMARY data
for col in summary_df.columns:
    description = summary_df[col].isnull().describe()
    if (description.top == True) and (description.freq == summary_df[col].isnull().count()):
        del summary_df[col]

		
#adjust time by offset for SUMMARY data


#remove unsed columns from SUMMARY data
summary_df.drop(['pkg_name','datauuid','extra_data'], axis=1, inplace=True)

#remove longest_idle_time==-1 rows (contain no useful data)
summary_df.drop(summary_df[summary_df['longest_idle_time'] == -1].index, inplace=True)




#######CREATE AGGRAGATED DAILY DF
#SLEEP data
sleep_agg = sleep_df.copy()
sleep_agg['date'] = sleep_agg['local_end_time'].dt.date
sleep_agg['duration_hr'] = (sleep_agg['local_end_time'] - sleep_agg['local_start_time'])/np.timedelta64(1, 'h')
sleep_agg.drop(['time_offset', 'deviceuuid', 'local_start_time', 'local_end_time'], axis=1, inplace=True)
sleep_agg2 = sleep_agg[['date', 'efficiency', 'quality']].groupby('date').mean()
sleep_agg = sleep_agg[['date', 'duration_hr']].groupby('date').sum()
sleep_agg = sleep_agg.join(sleep_agg2, on='date')
sleep_agg.rename(index=str, inplace=True, columns={'efficiency':'mean_sleep_efficiency', 'duration_hr':'total_sleep_duration_hr', 'quality':'mean_sleep_quality'})


#STEP_COUNT data
step_agg = step_count_df.copy()
step_agg['date'] = step_agg['local_start_time'].dt.date
step_agg.drop(['time_offset', 'deviceuuid', 'local_start_time', 'local_end_time', 'sample_position_type'], axis=1, inplace=True)
step_agg2 = step_agg[['date', 'speed']].groupby('date').mean()
step_agg = step_agg[['date', 'count', 'distance', 'calorie']].groupby('date').sum()
step_agg = step_agg.join(step_agg2, on='date')
step_agg.rename(index=str, inplace=True, columns={'count':'total_step_count', 'calorie':'total_step_calorie', 'speed':'mean_step_speed', 'distance':'total_step_distance'})

#FLOORS data
floors_agg = floors_df.copy()
floors_agg['date'] = floors_agg['local_end_time'].dt.date
floors_agg.drop(['time_offset', 'deviceuuid', 'local_start_time', 'local_end_time'], axis=1, inplace=True)
floors_agg = floors_agg.groupby('date').sum()
floors_agg.rename(index=str, inplace=True, columns={'floor':'total_floors_climbed'})

#HEART_RATE data
heart_agg = heart_rate_df.copy()
heart_agg['date'] = heart_agg['local_end_time'].dt.date
heart_agg.drop(['time_offset', 'deviceuuid', 'local_start_time', 'local_end_time'], axis=1, inplace=True)
heart_agg2 = heart_agg[['date','max']].groupby('date').max()
heart_agg3 = heart_agg[['date','min']].groupby('date').min()
heart_agg = heart_agg[['date','heart_rate']].groupby('date').mean()
heart_agg = heart_agg.join(heart_agg2, on='date')
heart_agg = heart_agg.join(heart_agg3, on='date')
heart_agg.rename(index=str, inplace=True, columns={'heart_rate':'mean_heart_rate', 'max':'max_heart_rate', 'min':'min_heart_rate'})

#EXERCISE data

exercise_agg = exercise_df.copy()
exercise_agg['date'] = exercise_agg['local_end_time'].dt.date
exercise_agg.drop(['time_offset', 'deviceuuid', 'local_start_time', 'local_end_time', 'exercise_type', 'count_type'], axis=1, inplace=True)
exercise_agg2 = exercise_agg[['date','max_altitude','max_heart_rate','max_cadence','max_speed']].groupby('date').max()
exercise_agg3 = exercise_agg[['date','min_altitude','min_heart_rate']].groupby('date').min()
exercise_agg4 = exercise_agg[['date','altitude_loss','count','altitude_gain','duration','incline_distance','decline_distance','calorie','distance']].groupby('date').sum()
exercise_agg = exercise_agg[['date','mean_heart_rate','mean_cadence','mean_speed']].groupby('date').mean()
exercise_agg = exercise_agg.join(exercise_agg2, on='date')
exercise_agg = exercise_agg.join(exercise_agg3, on='date')
exercise_agg = exercise_agg.join(exercise_agg4, on='date')
exercise_agg.rename(index=str, inplace=True, columns={'max_heart_rate':'max_exercises_heart_rate', 'max_speed':'max_exercises_speed',
                                                      'min_heart_rate':'min_exercises_heart_rate', 'count':'total_exercises_rep_count',
                                                      'duration':'total_exercises_duration', 'calorie':'total_exercises_calorie', 'distance': 
                                                      'total_exercises_distance', 'mean_heart_rate':'mean_exercises_heart_rate',
                                                      'mean_speed':'mean_exercises_speed'})

#combine to make DAILY AGGREGATED
daily_agg_df = sleep_agg.join(step_agg, on='date')
daily_agg_df = daily_agg_df.join(heart_agg, on='date')
daily_agg_df = daily_agg_df.join(exercise_agg, on='date')
daily_agg_df.reset_index(inplace=True)

#######export to new csv files
daily_agg_df.to_csv("cleaned_data/daily_aggregated.csv", sep=',', index=True)
exercise_df.to_csv("cleaned_data/exercise_cleaned.csv", sep=',', index=True)
floors_df.to_csv("cleaned_data/floors_climbed_cleaned.csv", sep=',', index=True)
heart_rate_df.to_csv("cleaned_data/heart_rate_cleaned.csv", sep=',', index=True)
sleep_df.to_csv("cleaned_data/sleep_cleaned.csv", sep=',', index=True)
step_count_df.to_csv("cleaned_data/step_count_cleaned.csv", sep=',', index=True)
summary_df.to_csv("cleaned_data/summary_cleaned.csv", sep=',', index=True)