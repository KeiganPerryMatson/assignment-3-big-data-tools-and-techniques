# Includes for user-defined classes
from SpotifyDataAccessor import SpotifyDataAccessor
from RedisDataAccessor import RedisDataAccessor

# Needed to load in .env file where Spotify API keys are stored
from dotenv import load_dotenv

# Needed to retrieve environment variables containing Spotify API keys
import os

# Needed for using dataframes
import pandas

# Needed for plotting data
import matplotlib.pyplot as plot

# Needed for plotting data
import seaborn as seaborn
import seaborn.objects as seaborn_objects

# Color codes for plotting data
red = '#ef4444'
green = '#84cc16'
orange = '#fb923c'
blue = '#22d3ee'
gray = '#475569'

######################################
# STEP 1: Read JSON from Spotify API #
######################################

# Load in the .env file and set up API key variables for use in the SpotifyDataAccessor class
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Initialize a SpotifyDataAccessor object, used to request data from the Spotify API
spotifyDataAccessor = SpotifyDataAccessor(client_id, client_secret)

# Initialize a RedisDataAccessor object, used to store and retrieve data from Redis
redisDataAccessor = RedisDataAccessor()

# Request an access token from Spotify
access_token = spotifyDataAccessor.requestAccessToken()

# Retrieve the top 10 tracks for different artists (returns Python dictionaries for each)
aerosmith_tracks = spotifyDataAccessor.getTopTracksForArtist(access_token, "Aerosmith")
acdc_tracks = spotifyDataAccessor.getTopTracksForArtist(access_token, "AC/DC")
black_sabbath_tracks = spotifyDataAccessor.getTopTracksForArtist(access_token, "Black Sabbath")
bon_jovi_tracks = spotifyDataAccessor.getTopTracksForArtist(access_token, "Bon Jovi")
guns_n_roses_tracks = spotifyDataAccessor.getTopTracksForArtist(access_token, "Guns N' Roses")
journey_tracks = spotifyDataAccessor.getTopTracksForArtist(access_token, "Journey")
kiss_tracks = spotifyDataAccessor.getTopTracksForArtist(access_token, "KISS")
metallica_tracks = spotifyDataAccessor.getTopTracksForArtist(access_token, "Metallica")
motley_crue_tracks = spotifyDataAccessor.getTopTracksForArtist(access_token, "Mötley Crüe")
van_halen_tracks = spotifyDataAccessor.getTopTracksForArtist(access_token, "Van Halen")

#################################
# STEP 2: Insert Into RedisJSON #
#################################

# Define a key value to use for inserting unique key values into the Redis database
key_index = 0

# Store the top 10 tracks for each artist
key_index = redisDataAccessor.storeTracks(key_index, aerosmith_tracks)
key_index = redisDataAccessor.storeTracks(key_index, acdc_tracks)
key_index = redisDataAccessor.storeTracks(key_index, black_sabbath_tracks)
key_index = redisDataAccessor.storeTracks(key_index, bon_jovi_tracks)
key_index = redisDataAccessor.storeTracks(key_index, guns_n_roses_tracks)
key_index = redisDataAccessor.storeTracks(key_index, journey_tracks)
key_index = redisDataAccessor.storeTracks(key_index, kiss_tracks)
key_index = redisDataAccessor.storeTracks(key_index, metallica_tracks)
key_index = redisDataAccessor.storeTracks(key_index, motley_crue_tracks)
key_index = redisDataAccessor.storeTracks(key_index, van_halen_tracks)

############################
# STEP 3: Perform Analysis #
############################

# Populate a Pandas dataframe with all of the items in the Redis database
track_dataframe = redisDataAccessor.populateDataFrame()

#######################################
# ANALYSIS 1: Duration VS. Popularity #
#######################################

# Copy into a new dataframe with duration and popularity
duration_dataframe = track_dataframe[["Duration (ms)", "Popularity"]].copy()

# Plot a line graph for duration vs. popularity to see if track length has a correlation with popularity
(seaborn_objects.Plot(data = duration_dataframe, x = "Popularity", y = "Duration (ms)")
                    .add(seaborn_objects.Dot(alpha = 0.5, color = red))
                    .add(seaborn_objects.Line(color = red, linewidth = 3), seaborn_objects.PolyFit(order = 1))
                    .label(x = "Popularity (0 - 100)", y = "Duration (ms)")
                    .theme({**seaborn.axes_style("whitegrid"), "grid.linestyle": ":"})).show()

# This dataset seems to show that tracks around the 250,000 ms duration (about 4 minutes) tend to be more popular

################################################
# ANALYSIS 2: Explicit Language VS. Popularity #
################################################

# Copy into a new dataframe with explicit language and popularity
explicit_dataframe = track_dataframe[["Explicit", "Popularity"]].copy()

# Plot a line graph for explicit vs. popularity to see if explicit language has a correlation with popularity
(seaborn_objects.Plot(data = explicit_dataframe, x = "Popularity", y = "Explicit")
                    .add(seaborn_objects.Dot(alpha = 0.5, color = red))
                    .add(seaborn_objects.Line(color = red, linewidth = 3), seaborn_objects.PolyFit(order = 1))
                    .label(x = "Popularity (0 - 100)", y = "Explicit (true / false)")
                    .theme({**seaborn.axes_style("whitegrid"), "grid.linestyle": ":"})).show()

# This dataset seems to show that tracks without explicit language tend to be more popular

#####################################
# ANALYSIS 3: Artist VS. Popularity #
#####################################

# Copy into a new dataframe with artist names and popularity
artist_dataframe = track_dataframe[["Artist Name", "Popularity"]].copy()

# Plot a dot plot graph to see which artist has higher popularity
(seaborn_objects.Plot(data = artist_dataframe, x = 'Artist Name', y = 'Popularity')
                    .add(seaborn_objects.Dot(alpha = 0.5, color = red))
                    .label(x = 'Artist Name', y = 'Popularity (0 - 100)')
                    .theme({**seaborn.axes_style("whitegrid"), "grid.linestyle": ":"})).show()

# This dataset seems to show that for the 10 selected artists:
#     - Black Sabbath and KISS generally had the lowest popularity
#     - AC/DC, Guns N' Roses, and Bon Jovi generally had the highest popularity
