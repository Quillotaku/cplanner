import pandas as pd
from datetime import datetime, timedelta
import sys
from tabulate import tabulate
from termcolor import colored

# Assuming your CSV data is stored in a file named 'movies.csv'
# You may need to adjust the file path accordingly
# file_path = 'movies.csv'
# print(sys.argv[1])

# Read the CSV file into a DataFrame
df = pd.read_csv(sys.argv[1])

# Convert the 'Duration' column to timedelta format
df['Duration'] = pd.to_timedelta(df['Duration'])

# Convert the 'Session' column to datetime format
df['Session'] = pd.to_datetime(df['Session'], format='%H:%M:%S')

# add 10 minutes to df['Duration']
df['Duration'] = df['Duration'] + timedelta(minutes=10)

# Sort the DataFrame by session start times
df_sorted = df.sort_values(by='Session')

# Initialize variables
selected_movies = []
end_time = datetime.min

# Initialize a list to store the selected movie sessions
selected_sessions_list = []

# Iterate through the sorted DataFrame and select non-overlapping movies
for index, row in df_sorted.iterrows():
    start_time = row['Session']
    movie_duration = row['Duration']
    if start_time >= end_time and row['Movie'] not in selected_movies:
        selected_movies.append(row['Movie'])
        selected_sessions_list.append(row[['Movie', 'Session', 'Duration']])
        end_time = start_time + movie_duration
    else:
        # print(f"Skipping {row['Movie']} at {start_time}, overlaps with the previous selection or already selected.")
        pass

# Create a DataFrame from the list of selected movie sessions
selected_sessions_df = pd.DataFrame(selected_sessions_list)
selected_sessions_df['Session'] = selected_sessions_df['Session'].dt.strftime('%H:%M:%S')
selected_sessions_df['Duration'] = pd.to_timedelta(selected_sessions_df['Duration'])
selected_sessions_df['Duration'] = selected_sessions_df['Duration'].apply(lambda x: f"{x.components.hours:02}:{x.components.minutes:02}:{x.components.seconds:02}")


c_selected_sessions_df = selected_sessions_df.copy()


headers = c_selected_sessions_df.columns
c_selected_sessions_df.columns = [colored(header, 'cyan') for header in headers]

for column in c_selected_sessions_df.columns:
    c_selected_sessions_df[column] = c_selected_sessions_df[column].apply(lambda x: colored(x, 'yellow'))

# Print the selected movies and their sessions
print(colored("\nSelected Movies and Sessions:\n",'green'))
print(tabulate(c_selected_sessions_df[c_selected_sessions_df.columns].values,headers=c_selected_sessions_df.columns, tablefmt='grid',))

# Print the total duration of the selected movies
total_duration_hours = sum(pd.to_timedelta(selected_sessions_df['Duration']), timedelta()).components.hours
total_duration_minutes = sum(pd.to_timedelta(selected_sessions_df['Duration']), timedelta()).components.minutes
print(colored(f'\nTotal Duration: {total_duration_hours}:{total_duration_minutes}\n','light_green'))
