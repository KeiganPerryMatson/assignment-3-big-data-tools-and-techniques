# Needed to access Redis database 
import redis

# Needed to access config.yaml file containing connection credentials for the Redis database
import yaml

def loadConfig():

    """
    FUNCTION ABSTRACT: loadConfig()

    DESCRIPTION: This function loads the configuration from the YAML file.

    ARGS: None

    RETURNS: dict - configuration data
    """

    # Open the config.yaml file in read format
    with open("config.yaml", "r") as file:

        # Return the loaded configuration data
        return yaml.safe_load(file)

def getRedisConnection():

    """
    FUNCTION ABSTRACT: getRedisConnection()
    
    DESCRIPTION: This function creates a Redis database connection using the configuration.

    ARGS: None

    RETURNS: Redis - Redis connection object
    """

    # Return a Redis database connection instance using the configuration credentials from config.yaml
    return redis.Redis(
        host = config["redis"]["host"],
        port = config["redis"]["port"],
        db = 0,
        decode_responses = True,
        username = config["redis"]["user"],
        password = config["redis"]["password"]
    )

# Call loadConfig() to load the configuration from the config.yaml file
config = loadConfig()