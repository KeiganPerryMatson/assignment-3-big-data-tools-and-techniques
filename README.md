# Assignment 3 - Big Data Tools & Techniques

## Prompt

Create a Python application that:

- Reads JSON from an API
- Inserts into a RedisJSON database
- Does some processing (3 outputs) such as matplotlib charts, aggregation, search, etc.

The Python application should be:

- Using Python classes (not plain scripting as shown in lecture notes)
- Should contain necessary docstrings
- Should be aligned properly
- Code should be pushed to a GitHub public repository (not uploaded)

Submit the following:

- GitHub URL
- Capture input / output as screenshots (should be clearly visible), add it to Google Doc, and share the URL

Follow the URL guidelines (clickable, shared, and no email notification).

Just a friendly heads-up: for EACH little slip-up, like Python classes, missing docstrings, uploading manually to GitHub, messy code alignment, URL guidelines, you'll lose 5 points.

## Execution

For this assignment, I decided to use the Spotify for Developers API to query for JSON data related to different musical artists' most popular songs. A Redis database is utilized to store and retrieve the data thereafter. With all data retrieved, I perform an analysis on how the popularity of various artist's top 10 tracks relates to duration and the kind of explicit language used in the tracks, as well as how the artists I chose compare to one another in their tracks' popularity. This analysis outputs sequentially at the end of the program in the form of 3 graphs displayed one after the other.

## Set-Up

In order to run this code, please do the following:

- Clone this GitHUB repository locally by running the following in a command prompt window: git clone https://github.com/KeiganPerryMatson/assignment-3-big-data-tools-and-techniques.git
- Ensure that you have the following Python libraries installed on your local machine: python-dotenv, os, pandas, matplotlib, seaborn, base64, requests, json, redis
- Rename the config.yaml_template file to config.yaml and the .env_template file to .env
- For the config.yaml file, you will need to substitute in details from your personal Redis database. You can retrieve these details by creating a Redis database at https://app.redislabs.com
- For the .env file, you will need to substitute in a client ID key and client secret key from Spotify. You can retrieve these keys by creating an app at https://developer.spotify.com
- Run the application by navigating into the newly generated directory and running python ./main.py
