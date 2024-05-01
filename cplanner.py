import pandas as pd
from datetime import datetime, timedelta
import sys
from tabulate import tabulate
from termcolor import colored
import re

# check included or excluded movies with regex to ease the input on the user
def check_movie(movie, patterns):
    for pattern in patterns:
        if re.search(pattern, movie, re.IGNORECASE):
            return True
    return False

# Initialize variables
selected_movies = []
excluded_movies = []
included_movies = []
selected_sessions_list = []
end_time = datetime.min
try:
    if sys.argv[2] == '--exclude':
        excluded_movies = sys.argv[3].split(',')
    elif sys.argv[2] == '--include':
        included_movies = sys.argv[3].split(',')
except:
    pass

# Read the CSV file into a DataFrame, convert the 'Duration' column to timedelta format, convert the 'Session' column to datetime format
# add 10 minutes to df['Duration'] for the trailers before the movie and sort the DataFrame by session start times
df = pd.read_csv(sys.argv[1])
df['Duration'] = pd.to_timedelta(df['Duration'])
df['Session'] = pd.to_datetime(df['Session'], format='%H:%M:%S')
df['Duration'] = df['Duration'] + timedelta(minutes=10)
df_sorted = df.sort_values(by='Session')

# Iterate through the sorted DataFrame and select non-overlapping movies and include or exclude movies depending on the variables initialized
for index, row in df_sorted.iterrows():
    start_time = row['Session']
    movie_duration = row['Duration']
    if (not included_movies or check_movie(row['Movie'],included_movies)) and not check_movie(row['Movie'],excluded_movies):
        if start_time >= end_time and row['Movie'] not in selected_movies:
            selected_movies.append(row['Movie'])
            selected_sessions_list.append(row[['Movie', 'Session', 'Duration']])
            end_time = start_time + movie_duration


# Create a DataFrame from the list of selected movie sessions, Duration and Session in the format HH:MM:SS
selected_sessions_df = pd.DataFrame(selected_sessions_list)
selected_sessions_df['Session'] = selected_sessions_df['Session'].dt.strftime('%H:%M:%S')
selected_sessions_df['Duration'] = pd.to_timedelta(selected_sessions_df['Duration'])
selected_sessions_df['Duration'] = selected_sessions_df['Duration'].apply(lambda x: f"{x.components.hours:02}:{x.components.minutes:02}:{x.components.seconds:02}")

#Copy the selected_sessions to add color just to print it in a nice way
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