import json
import urllib
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
    
    res = None
    resp = await requests.post(f'{url}card/list', headers=headers, data=json.dumps(data))
    try:
        res = await resp.json()
        if "error" in res:
            return res["error"]["message"]
        return res
    except Exception as e:
        print(e)
        return None
    

async def get_item_info(token, nm_id: int) -> dict:
    headers = {'Authorization': token}
    data = {
        "params":{
            "query":{
                "limit":1,
                "offset":0
            },
            "filter":{
                "order":{
                    "column":"createdAt",
                    "order":"desc"
                },
                "find":[
                    {
                    "column":"nomenclatures.nmId",
                    "search":int(nm_id)
                    }
                ]
            }
        },
        "jsonrpc":"2.0",
        "id":1
    }
            
    resp = await requests.post(f'{url}card/list', headers=headers, data=json.dumps(data))
    try:
        res = await resp.json()
        return res
    except:
        return None

async def change_item_name(token, nm_id, name, country = ''):
    headers = {'Authorization': token}
    res = await get_item_info(token, nm_id)
    if res == None:
        return None
        
    card = res["result"]["cards"][0]

    for i in range(len(card["addin"])):
        if(card["addin"][i]["type"] == "Наименование"): card["addin"][i]["params"][0]["value"] = name; break;

    if country != 'void' and card["countryProduction"] == "":
        card["countryProduction"] = country

    data = {
        "id":1,
        "jsonrpc":"2.0",
        "params":{
            "card": card
        }
    }

    resp = await requests.post(f'{url}card/update', headers=headers, data=json.dumps(data))
    try:
        res = await resp.json()
        if "error" in res:
            return res["error"]["message"]
        return res
    except:
        return None


async def country_list(token, char):
    headers = {'Authorization': token}

    try:
        resp = await requests.get(f'{url}api/v1/directory/countries?top=100&pattern={char}', headers=headers)
        res = await resp.json()
        if not res["error"]:
            return res["data"]
    except:
        return []