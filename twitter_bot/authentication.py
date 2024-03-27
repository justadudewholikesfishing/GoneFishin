import json
import os
from requests_oauthlib import OAuth1Session


# File to save credentials
CREDENTIALS_FILE = "twitter_credentials.json"

def authenticate():
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")

    if consumer_key is None or consumer_secret is None:
        print("Consumer key or consumer secret is missing.")

    # Check if credentials file exists
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"Please create {CREDENTIALS_FILE} file with the following content:")
        content = """
{
    "consumer_key": "YOUR_CONSUMER_KEY",
    "consumer_secret": "YOUR_CONSUMER_SECRET",
}
        """
        print(content)
        raise Exception("Credentials file not exists")

    with open(CREDENTIALS_FILE, 'r') as file:
        creds = json.load(file)

    if("consumer_key" in creds and "consumer_secret" in creds and "access_token" in creds and "access_token_secret" in creds):
        return creds["consumer_key"], creds["consumer_secret"], creds["access_token"], creds["access_token_secret"]

    # Otherwise proceed with authentication
    # Get request token
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
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
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    # Save the credentials to a file
    with open(CREDENTIALS_FILE, 'w') as file:
        json.dump({
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
            "access_token": access_token,
            "access_token_secret": access_token_secret
        }, file)

    return consumer_key, consumer_secret, access_token, access_token_secret

if __name__ == '__main__':
    authenticate()
    