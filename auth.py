from uuid import uuid4
import json, os, urllib.request, base64

# get the authorization token to make requests to Spotify API
def get_auth_token():

    # Check to see which environment to use by reading from config file
    with open("config.json", "r") as config_file:
       config = json.load(config_file)
       if not config["prod"]:
           with open("spotify_token.json", "r") as auth_file:
               auth_data = json.load(auth_file)
               client_id = auth_data["client_id"]
               client_secret = auth_data["client_secret"]
       else:
           client_id = os.environ["CLIENT_ID"]
           client_secret = os.environ["CLIENT_SECRET"]

    # Spotify requires base64 encoding for the token
    auth_token = client_id + ":" + client_secret
    auth_token_encoded = base64.b64encode(auth_token.encode("ascii"))

    request_body = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
    auth_request = urllib.request.Request("https://accounts.spotify.com/api/token", data=request_body)
    auth_request.add_header("Authorization", "Basic " + auth_token_encoded.decode())

    try:
       auth_response = json.loads(urllib.request.urlopen(auth_request).read())
    except urllib.error.HTTPError as err:
       print(err.read())

    access_token = auth_response["access_token"]

    return access_token

