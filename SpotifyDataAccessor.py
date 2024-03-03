# Needed for encoding Spotify API access token request data
import base64 

# Needed for sending HTTP requests to Spotify API
from requests import post, get

# Needed to utilize JSON data returned by Spotify API containing access token
import json

class SpotifyDataAccessor:

    """
    CLASS ABSTRACT: SpotifyDataAccessor

    DESCRIPTION: This class utilizes the Spotify API to query and retrieve data.
    """

    def __init__(self, client_id, client_secret):

        """
        FUNCTION ABSTRACT: Constructor

        DESCRIPTION: Creates an object of type SpotifyDataAccessor.

        ARGS:
            self - the class object
            client_id - client ID key from Spotify developer account
            client_secret - client secret key from Spotify developer account

        RETURNS: None
        """

        self.__client_id = client_id
        self.__client_secret = client_secret

    def requestAccessToken(self):
        
        """
        FUNCTION ABSTRACT: requestAccessToken()

        DESCRIPTION: This function builds and sends a POST request to receive an access token from the Spotify API.

        ARGS: self - the class object

        RETURNS: access_token - access token retrieved from Spotify API
        """

        # Define an authorization string in Spotify's expected format
        auth_string = self.__client_id + ":" + self.__client_secret

        # Encode the authorization string in Spotify's expected encoding
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        # Define the URL to request an access key from
        url = "https://accounts.spotify.com/api/token"

        # Define the headers necessary for the POST request to the above URL
        headers = {"Authorization": "Basic " + auth_base64, "Content-Type": "application/x-www-form-urlencoded"}

        # Define the data necessary for the POST request to the above URL
        data = {"grant_type": "client_credentials"}

        # Send a POST request to the Spotify API to receive an access token (returned in JSON format / stored in request.content)
        request = post(url, headers = headers, data = data)

        # Convert received JSON data into a Python dictionary by using json.loads (load from string)
        json_request = json.loads(request.content)

        # Retrieve the access token from the json_request Python dictionary
        access_token = json_request["access_token"]

        # Return the access token
        return access_token
    
    def getAuthorizationHeader(self, access_token):

        """
        FUNCTION ABSTRACT: getAuthorizationHeader()

        DESCRIPTION: This function returns the authorization header needed for any requests to the Spotify API.

        ARGS:
            self - the class object
            access_token - access token retrieved from Spotify API

        RETURNS: authorization header - expected header for any POST requests to the Spotify API
        """

        return {"Authorization": "Bearer " + access_token}
    
    def checkTypeLegalities(self, type):

        """
        FUNCTION ABSTRACT: checkTypeLegalities()

        DESCRIPTION: This function determines whether a legal type was passed (artist, album, or track).

        ARGS:
            self - the class object
            type - type of query requested (artist, album, or track)

        RETURNS: legality_check - boolean flag (True = pass, False = fail)
        """

        # Define a flag to check for a legal type (album, artist, track)
        legality_check = True

        # If a proper type was not given...
        if ((type != "album") and (type != "artist") and (type != "track")):

            # Set the flag to false to trigger exiting the calling function
            legality_check = False
        
        # Return the result of the type legality check
        return legality_check
    
    def getSpotifyData(self, access_token, name, type):

        """
        FUNCTION ABSTRACT: getSpotifyData()

        DESCRIPTION:
            This function queries the Spotify API with a provided name of an artist, album, or track
            to retrieve the data associated with the item.

        ARGS:
            self - the class object
            access_token - access token retrieved from Spotify API
            name - name of the item
            type - type of item (artist, album, or track)

        RETURNS: json_request[0] - Python dictionary containing the data associated with the item
        """

        # If a proper type was not given...
        if (self.checkTypeLegalities(type) == False):

            # A proper type was not given. Output an error message and exit the function.
            print("ERROR: A proper type was not given. Please define a valid type (artist, album, or track)...")

            return None

        # Define the URL to request a Spotify ID from
        url = "https://api.spotify.com/v1/search"

        # Call getAuthorizationHeader() to get the headers necessary for the GET request to the above URL
        headers = self.getAuthorizationHeader(access_token)

        # Define the query that the Spotify API will use to get a specified item's ID (will always grab the most popular item match)
        query = f"?q={name}&type={type}&limit=1"

        # Combine the URL and the query into in Spotify's expected format
        query_url = url + query

        # Send a GET request to the Spotify API to receive an item id (returned in JSON format / stored in request.content)
        request = get(query_url, headers = headers)

        # Convert received JSON data into a Python dictionary by using json.loads (load from string)
        json_request = json.loads(request.content)[type + "s"]["items"]

        # If the GET request returned nothing...
        if len(json_request) == 0:

            # Spotify could not find an item with this name. Output an error message and exit the function
            print("ERROR: No item with this name exists...")

            return None

        # Return the data retrieved for this item
        return json_request[0]

    def getTopTracksForArtist(self, access_token, artist_name):

        """
        FUNCTION ABSTRACT: getTopTracksForArtist()

        DESCRIPTION:
            This function queries the Spotify API with a provided artist's name and retrieves their
            top 10 most popular tracks.

        ARGS:
            self - the class object
            access_token - access token retrieved from Spotify API
            artist_name - name of the artist

        RETURNS:
            json_request - Python dictionary containing the following relevant fields:
                + album - the album the track is on (Python dictionary that contains multiple fields)
                + artists - the artist(s) of the track (Python dictionary that contains multiple fields)
                + duration_ms - duration of the track in miliseconds for the track
                + explicit - flag for whether the track has explicit language or not (True = explicit, False = not explicit)
                + id - Spotify ID for the track
                + name - name of the track
                + popularity - popularity score for the track (0 - 100)
                + track_number - number of the track on the album
        """

        # Call getSpotifyData() to get the data for a specified artist
        artist = self.getSpotifyData(access_token, artist_name, "artist")

        # If no items were retrieved for this artist...
        if (artist == None):

            # Spotify could not find an artist with this name. Output an error message and exit the function
            print("ERROR: Could not retrieve top tracks for this artist...")

            return NoneS
        
        # Retrieve the artist's ID from the artist Python dictionary
        artist_id = artist["id"]
        
        # Define the URL to request the artist's top 10 tracks from, using the artist_id retrieved from getSpotifyData()
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"

        # Call getAuthorizationHeader() to get the headers necessary for the GET request to the above URL
        headers = self.getAuthorizationHeader(access_token)

        # Send a GET request to the Spotify API to receive an artist's top 10 tracks (returned in JSON format / stored in request.content)
        request = get(url, headers = headers)

        # Convert received JSON data into a Python dictionary by using json.loads (load from string)
        json_request = json.loads(request.content)["tracks"]

        # Return the Python dictionary containing the top 10 tracks retrieved for this artist
        return json_request
