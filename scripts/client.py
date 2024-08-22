import json
import requests
import helper.constants as CNST

class API():
    """A class used to interact with an API by managing access tokens and sending requests."""

    def __init__(self):
        """Initializes the API class instance. Currently, no initialization logic is required."""
        pass

    def get_access_token(self):
        """Requests and retrieves an access token from the API.nThis method makes a POST request to the 
        token URL with the client ID and client secret in the request body.

        Returns:
            str: The access token retrieved from the API response.
        """
        CNST.TOKEN_REQUEST_BODY['client_id'] = CNST.CLIENT_ID
        CNST.TOKEN_REQUEST_BODY['client_secret'] = CNST.CLIENT_SECRET

        response = requests.request("POST",
                                    url=CNST.TOKEN_URL,
                                    headers=CNST.TOKEN_HEADER,
                                    data=CNST.TOKEN_REQUEST_BODY)
        
        access_token = response.json()['access_token']

        return access_token
    
    def get_data(self):
        """Fetches data from the API using the provided access token.

        Returns:
            dict: The JSON data retrieved from the API response.
        """
        url = CNST.API.replace("<PLACE_HOLDER>", CNST.PLACE_HOLDER.replace("<PLAYLIST_ID>", CNST.PLAYLIST_ID))
        CNST.API_HEADER["Authorization"] = CNST.API_HEADER["Authorization"].replace("<ACCESS_TOKEN>", self.get_access_token())

        response = requests.request('GET', 
                                    url = url,
                                    headers = CNST.API_HEADER)
        data = response.json()
        return data
    
if __name__ == '__main__':
    api_instance = API()
    
    token = api_instance.get_access_token()
    print(f"Access Token: {token}")

    data = api_instance.get_data()
    print(f"Data: {json.dumps(data, indent=4)}")