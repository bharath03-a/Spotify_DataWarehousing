import json
import scripts.client as cl
import helper.constants as CNT

api_instance = cl.API()
    
token = api_instance.get_access_token()
print(f"Access Token: {token}")

data, keys = api_instance.get_data()
print(f"Data: {len(data)}")
print(f"Keys: {keys}")