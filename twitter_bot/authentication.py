import json
import os
from requests_oauthlib import OAuth1Session


# File to save credentials
CREDENTIALS_FILE = "twitter_credentials.json"

def authenticate():

    # Check if credentials file exists
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"Please create {CREDENTIALS_FILE} file with the following content:")
        content = """
{
    "api_key": "YOUR_CONSUMER_KEY",
    "api_key_secret": "YOUR_CONSUMER_SECRET",
}
        """
        print(content)
        raise Exception("Credentials file not exists")

    with open(CREDENTIALS_FILE, 'r') as file:
        creds = json.load(file)

    if("api_key" in creds and "api_key_secret" in creds and "access_token" in creds and "access_token_secret" in creds):
        return creds["api_key"], creds["api_key_secret"], creds["access_token"], creds["access_token_secret"]

    if(not "api_key" in creds):
        raise Exception("api_key is missing from {CREDENTIALS_FILE}")

    if(not "api_key_secret" in creds):
        raise Exception("api_key_secret is missing from {CREDENTIALS_FILE}")
    
    # Otherwise proceed with authentication
    # Get request token
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(creds["api_key"], client_secret=creds["api_key_secret"])
    fetch_response = oauth.fetch_request_token(request_token_url)

    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")

    # Get authorization
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    
    print("Please go here and authorize:", authorization_url)
    verifier = input("Paste the PIN here: ")

    # Get the access token
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        creds["api_key"],
        client_secret=creds["api_key_secret"],
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    creds["access_token"] = oauth_tokens["oauth_token"]
    creds["access_token_secret"] = oauth_tokens["oauth_token_secret"]

    # Save the credentials to a file
    with open(CREDENTIALS_FILE, 'w') as file:
        json.dump(creds, file, indent=4)

    return creds["api_key"], creds["api_key_secret"], creds["access_token"], creds["access_token_secret"]

if __name__ == '__main__':
    authenticate()
    