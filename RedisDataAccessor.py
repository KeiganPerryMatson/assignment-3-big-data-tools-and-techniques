# Needed for establishing a connection to the Redis database
from db_config import getRedisConnection

# Needed to serialize JSON strings
import json

# Needed to insert JSON values into the Redis database
from redis.commands.json.path import Path

# Needed for using dataframes
import pandas

class RedisDataAccessor:

    """
    CLASS ABSTRACT: RedisDataAccessor

    DESCRIPTION: This class stores and retrieves data from the Redis database. 
    """

    def __init__(self):

        """
        FUNCTION ABSTRACT: Constructor

        DESCRIPTION: Creates an object of type RedisDataAccessor.

        ARGS: self - the class object

        RETURNS: None
        """

        # Initialize the Redis database connection
        self.__redis_connection = getRedisConnection()

        # Flush all records from the Redis database for a fresh run
        self.__redis_connection.flushall()

    def storeTracks(self, key, tracks):

        """
        FUNCTION ABSTRACT: storeTracks()

        DESCRIPTION: This function uses the Redis database connection to store a Python dictionary
                     of tracks.

        ARGS:
            self - the class object
            key - the current numerical key for the tracks (i.e. the next index in the Redis database)
            tracks - the tracks to store

        RETURNS: updated_key - the updated numerical key for the tracks
        """

        # Save off the key at its current numerical value for incrementing (needed to create unique key values for each track)
        updated_key = key

        # For each track in tracks...
        for track in tracks:

            # Use the key value passed in to create a unique key value (this is why we declare a key_index in main.py and pass / return it)
            formatted_key = f"track:{updated_key}"

            # Store the key / track pair in the Redis database
            self.__redis_connection.json().set(formatted_key, Path.root_path(), track)

            # Increment the key index
            updated_key = updated_key + 1

        # Return the updated key index, now adjusted for however many tracks were saved off
        return updated_key

    def retrieveTrack(self, key):

        """
        FUNCTION ABSTRACT: retrieveTrack()

        DESCRIPTION: This function uses the Redis database connection to retrieve a singular track using a given key.

        ARGS:
            self - the class object
            key - the already-formatted key for the requested track

        RETURNS: track - the track retrieved from the Redis database for the given key
        """

        # Retrieve the track from the Redis database
        track = self.__redis_connection.json().get(key)

        # Return the retrieved track
        return track
    
    def populateDataFrame(self):

        """
        FUNCTION ABSTRACT: populateDataFrame()

        DESCRIPTION: This function inserts data retrieved from the Redis database into a passed-in Pandas dataframe.

        ARGS: self - the class object

        RETURNS:
            populated_dataframe - a dataframe containing all of the records from the Redis database
        """

        # Define an empty list to pack with each Redis database item
        track_list = []

        # For every key in the Redis database...
        for key in self.__redis_connection.scan_iter("track:*"):

            # Call retrieveTrack() to retrieve the track stored under that specific key
            track = self.retrieveTrack(key)

            # For each item in the ["artists"] list in the track...
            for item in track["artists"]:

                # Save the artist's name (this is done only for artists because this particular element of track is uniquely formatted as a list)
                artist_name = item["name"]

            # Format the row of data to be saved off in the list
            formatted_row = {
                "Track Name": track["name"],
                "Artist Name": artist_name,
                "Album Name": track["album"]["name"],
                "Duration (ms)": track["duration_ms"],
                "Explicit": track["explicit"],
                "Popularity": track["popularity"]
            }

            # Append the formatted row onto the list
            track_list.append(formatted_row)

        # Define a dataframe using the list created above
        populated_dataframe = pandas.DataFrame.from_dict(track_list)

        # Return the populated dataframe
        return populated_dataframe
