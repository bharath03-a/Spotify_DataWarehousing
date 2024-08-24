import json
import requests
import helper.constants as CNST

class API():
    """A class used to interact with an API by managing access tokens and sending requests."""

    def __init__(self):
        """Initializes the API class instance. Currently, no initialization logic is required."""
        self.item_keys = set()
        self.all_data = []

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
    
    def extract_keys(self, d, keys_set):
        """
        Recursively extracting all keys from a nested dictionary and add them to a set.

        Args:
            d (dict): The dictionary from which to extract keys.
            keys_set (set): The set to store all unique keys.
        """
        for k, v in d.items():
            keys_set.add(k)
            if isinstance(v, dict):
                self.extract_keys(v, keys_set)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        self.extract_keys(item, keys_set)
    
    def get_data(self):
        """Fetches data from the API using the provided access token.

        Returns:
            tuple: A tuple containing the list of all items and a set of all keys.
        """
        offset = 0
        limit = 30

        while offset <= 1000:
            url = CNST.API.replace("<PLACE_HOLDER>", CNST.PLACE_HOLDER.replace("<PLAYLIST_ID>", CNST.PLAYLIST_ID))
            url += f"?offset={offset}&limit={limit}"
            
            CNST.API_HEADER["Authorization"] = CNST.API_HEADER["Authorization"].replace("<ACCESS_TOKEN>", self.get_access_token())

            response = requests.request('GET', 
                                        url=url,
                                        headers=CNST.API_HEADER)
            data = response.json()

            items = data.get('items', [])
            if items:
                for item in items:
                    self.extract_keys(item, self.item_keys)

            if not items or len(items) < limit:
                self.all_data.extend(items)
                break

            self.all_data.extend(items)
            offset += limit

        return self.all_data, self.item_keys
    
    def flatten_dict(self, d, parent_key='', sep='_', exclude_keys=None):
        """Flattens a nested dictionary.

        Args:
            d (dict): The dictionary to flatten.
            parent_key (str): The base key string to use for flattened keys.
            sep (str): The separator to use between parent and child keys.
            exclude_keys (set): A set of keys to exclude from the flattened dictionary.

        Returns:
            dict: A flattened dictionary with no nested structures.
        """
        exclude_keys = exclude_keys or set()
        items = []
        for k, v in d.items():
            if k in exclude_keys:
                continue
            new_key = f'{parent_key}{sep}{k}' if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep, exclude_keys=exclude_keys).items())
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(self.flatten_dict(item, f'{new_key}_{i}', sep=sep, exclude_keys=exclude_keys).items())
                    else:
                        items.append((f'{new_key}_{i}', item))
            else:
                items.append((new_key, v))
        return dict(items)
    
if __name__ == '__main__':
    api_instance = API()
    
    token = api_instance.get_access_token()
    print(f"Access Token: {token}")

    data, keys = api_instance.get_data()
    print(f"Data: {json.dumps(data, indent=4)}")
    print(f"Keys: {keys}")