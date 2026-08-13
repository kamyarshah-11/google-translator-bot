import requests
import json


def create_data(src, tgt, txt):
    return {"source": src, "target": tgt, "text": txt}


def sending_request(
    data,
    header,
    url,
):

    try:
        response = requests.post(url, headers=header, json=data)
        return response.json()["result"]
    except:
        return None


def url_header():
    with open("key.json", "r", encoding="utf-8") as file:
        config = json.load(file)
        HEADERS = config["headers"]
        URL = config["url"]
    return URL, HEADERS
