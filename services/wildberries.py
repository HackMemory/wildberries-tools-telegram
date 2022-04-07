import json
from aiohttp_requests import requests

url = 'https://suppliers-api.wildberries.ru/'

async def validate_token(token) -> bool:
    headers = {'Authorization': token}
    resp = await requests.post(f'{url}card/list', headers=headers)
    if "invalid token" in await resp.text():
        return False
    
    return True


async def get_cards_list(token, count = 10, offset = 0) -> dict:
    headers = {'Authorization': token}
    data = {
        "params":{
            "query":{
                "limit":count,
                "offset":offset
            },
             "filter":{
                "order":{
                    "column":"createdAt",
                    "order":"desc"
                },
             }
        },

        "jsonrpc":"2.0",
        "id":1
    }
    
    resp = await requests.post(f'{url}card/list', headers=headers, data=json.dumps(data))
    try:
        data = await resp.json()
        if "error" in data:
            return None
        return data

    except:
        return None
    

async def get_item_info(token, imt_id) -> dict:
    headers = {'Authorization': token}
    pass

async def change_item_name(token, imt_id, name) -> bool:
    headers = {'Authorization': token}
    pass