import pandas as pd
from datetime import datetime, timedelta
import sys

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
        print(f"Skipping {row['Movie']} at {start_time}, overlaps with the previous selection or already selected.")

# Create a DataFrame from the list of selected movie sessions
selected_sessions_df = pd.DataFrame(selected_sessions_list)

# Print the selected movies and their sessions
print("\nSelected Movies and Sessions:")
print(selected_sessions_df)

# Print the total duration of the selected movies
total_duration = sum(selected_sessions_df['Duration'], timedelta())
print("\nTotal Duration:", total_duration)
