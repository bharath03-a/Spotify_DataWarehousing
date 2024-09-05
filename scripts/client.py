import json
import requests
import helper.constants as CNST

class API():
    """A class used to interact with an API by managing access tokens and sending requests."""

    def __init__(self):
        """Initializes the API class instance. Currently, no initialization logic is required."""
        self.item_keys = {'PLAYLISTS' : set(),
                          'ARTISTS' : set(),
                          'AUDIO_FEATURES' : set()}
        self.all_data = {'PLAYLISTS' : [],
                          'ARTISTS' : [],
                          'AUDIO_FEATURES' : []}

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

    def get_spotify_data(self, api_type="PLAYLISTS", input_data=None):
        """Fetches data from the API using the provided access token.

        Args:
            api_type (str): The type of API data to fetch, either "PLAYLISTS" or other types.
            input_data (list): A list of input data for queries, if applicable.

        Returns:
            tuple: A tuple containing the list of all items and a set of all keys.
        """
        offset = 0
        limit = 25
        try:
            if api_type == "PLAYLISTS":
                while offset <= 1000:
                    url = CNST.API.replace("<PLACE_HOLDER>", CNST.PLAYLIST_API.replace("<PLAYLIST_ID>", CNST.PLAYLIST_ID))
                    url += f"?offset={offset}&limit={limit}"
                    CNST.API_HEADER["Authorization"] = CNST.API_HEADER["Authorization"].replace("<ACCESS_TOKEN>", self.get_access_token())

                    response = requests.get(url, headers=CNST.API_HEADER)
                    response.raise_for_status()

                    data = response.json()
                    items = data.get('items', [])
                    if items:
                        for item in items:
                            self.extract_keys(item, self.item_keys[api_type])

                    if not items or len(items) < limit:
                        self.all_data[api_type].extend(items)
                        break

                    self.all_data[api_type].extend(items)
                    offset += limit
            elif api_type == "AUDIO_ANALYSIS":
                # lot of technical details are present
                pass
            else:
                step = limit
                while offset < len(input_data):
                    values = ",".join(input_data[offset:step])
                    url = CNST.API.replace("<PLACE_HOLDER>", CNST.API_QUERY[api_type].replace("<IDS>", values))
                    CNST.API_HEADER["Authorization"] = CNST.API_HEADER["Authorization"].replace("<ACCESS_TOKEN>", self.get_access_token())

                    response = requests.get(url, headers=CNST.API_HEADER)
                    response.raise_for_status()

                    data = response.json()
                    items = data.get(api_type.lower(), [])
                    if items:
                        for item in items:
                            self.extract_keys(item, self.item_keys[api_type])

                    if not items or len(items) < limit:
                        self.all_data[api_type].extend(items)
                        break

                    self.all_data[api_type].extend(items)
                    offset += limit
                    step += limit

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        except ValueError as val_err:
            print(f"Value error occurred: {val_err}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return self.all_data[api_type], self.item_keys[api_type]

    def flatten_dict(self, d, parent_key='', sep='_', include_keys=None):
        """Flattens a nested dictionary.

        Args:
            d (dict): The dictionary to flatten.
            parent_key (str): The base key string to use for flattened keys.
            sep (str): The separator to use between parent and child keys.
            include_keys (set): A set of keys to include from the flattened dictionary.

        Returns:
            dict: A flattened dictionary with no nested structures.
        """
        include_keys = include_keys or set()
        items = []
        for k, v in d.items():
            if k not in include_keys:
                continue
            new_key = f'{parent_key}{sep}{k}' if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep, include_keys=include_keys).items())
            elif isinstance(v, list) and new_key != "track_artists":
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(self.flatten_dict(item, f'{new_key}_{i+1}', sep=sep, include_keys=include_keys).items())
                    else:
                        items.append((f'{new_key}_{i+1}', item))
            else:
                items.append((new_key, v))
        return dict(items)
    
if __name__ == '__main__':
    api_instance = API()
    
    token = api_instance.get_access_token()
    # print(f"Access Token: {token}")

    data, keys = api_instance.get_spotify_data(api_type="PLAYLISTS")
    # print(f"Keys: {keys}")