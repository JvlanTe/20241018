import requests
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
    query = {
        "app": app_id,
        "fields": [
            "staff_number",
            "name",
            "staff_address",
            "office_address",
        ],
    }

    response = requests.get(url, headers=headers, params=query)

    if response.status_code != 200:
        print("データを正常に取得できませんでした", response.status_code)
        return []

    records = response.json().get("records", [])
    return records


def main():
    records = get_kintone_records()
    if records:
        for record in records:
            staff_number = record.get("staff_number", {}).get("value", "")
            name = record.get("name", {}).get("value", "")
            staff_address = record.get("staff_address", {}).get("value", "")
            office_address = record.get("office_address", {}).get("value", "")

            print(f"職員番号:{staff_number},氏名:{name},職員住所:{staff_address},勤務先住所:{office_address}")
    else:
        print("レコードが見つかりません")


if __name__ == "__main__":
    main()
