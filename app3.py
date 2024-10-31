import requests
import time
import os
from dotenv import load_dotenv

load_dotenv(override=True)

subdomain = os.getenv("DOMAIN")

app_id = os.getenv("APP_ID_2")

api_token = os.getenv("API_2")

url = f"https://{subdomain}.cybozu.com/k/v1/records.json"


headers = {
    "X-Cybozu-API-Token": api_token,
}


def get_kintone_records():
    querystring = {
        "app": app_id,
        "fields": [
            "record_id",
            "staff_number",
            "name",
            "staff_address",
            "office_address",
        ],
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        print("データを正常に取得できませんでした", response.status_code)
        return []

    records = response.json().get("records", [])
    return records


def update_kintone_record(record_id, distance_km):
    url = f"https://{subdomain}.cybozu.com/k/v1/record.json"
    headers = {"X-Cybozu-API-Token": api_token, "Content-Type": "application/json"}

    data = {
        "app": app_id,
        "id": record_id,
        "record": {
            "distance": {"value": distance_km},
        },
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        print("データを正常に更新できました", response.status_code)
    else:
        print("データを正常に更新できませんでした", response.status_code)


# SearchAPIで住所情報を取得し、緯度経度を返す
def search_address(address):
    url = "https://mapfanapi-search.p.rapidapi.com/addr"
    headers = {
        "X-RapidAPI-Key": os.getenv("MAPFAN_API"),
        "X-RapidAPI-Host": "mapfanapi-search.p.rapidapi.com",
    }
    querystring = {"addr": address}
    time.sleep(1)
    response = requests.get(url, headers=headers, params=querystring)
    dic = response.json()
    # results配列の1件目を取得して緯度経度を取得
    lon = dic["results"][0]["lon"]
    lat = dic["results"][0]["lat"]
    # 経度,緯度に編集する
    lon_lat = f"{lon},{lat}"
    # 残り実行回数を取得
    search_remaining = response.headers["X-RateLimit-Requests-Remaining"]
    # 経度,緯度、残り実行回数を返す
    return lon_lat, search_remaining


# RouteAPIで最短経路を取得し、距離を返す
def select_route(start_lon_lat, end_lon_lat):
    totalDistance = 0
    url = "https://mapfanapi-route.p.rapidapi.com/calcroute"
    headers = {
        "X-RapidAPI-Key": os.getenv("MAPFAN_API"),
        "X-RapidAPI-Host": "mapfanapi-route.p.rapidapi.com",
    }
    querystring = {"start": start_lon_lat, "destination": end_lon_lat}
    time.sleep(1)
    response = requests.get(url, headers=headers, params=querystring)
    dic = response.json()
    # 距離を取得
    totalDistance = dic["summary"]["totalDistance"]
    # 残り実行回数を取得
    route_remaining = response.headers["X-RateLimit-Requests-Remaining"]
    # 距離、残り実行回数を返す
    return totalDistance, route_remaining


def is_empty(value):
    return value is None or not str(value).strip()


def main():
    # print(os.getenv("MAPFAN_API"))
    records = get_kintone_records()
    if records:
        for record in records:
            staff_address = record.get("staff_address", {}).get("value", "")
            office_address = record.get("office_address", {}).get("value", "")
            record_id = record.get("record_id", {}).get("value", "")
            staff_lon_lat, search_remaining = search_address(staff_address)
            office_lon_lat, search_remaining = search_address(office_address)
            totalDistance, route_remaining = select_route(staff_lon_lat, office_lon_lat)

            distance_km = round(totalDistance / 1000, 1)

            # print(distance_km)

            update_kintone_record(record_id, distance_km)

    else:
        print("レコードが見つかりません")


if __name__ == "__main__":
    main()
