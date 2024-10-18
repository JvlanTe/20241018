import requests
import json
import os
from dotenv import load_dotenv
import tkinter
from tkinter import Label, Entry, Button

load_dotenv()

subdomain = os.getenv("DOMAIN")

app_id = os.getenv("APP_ID")

api_token = os.getenv("API")

url = f"https://{subdomain}.cybozu.com/k/v1/record.json"

headers = {"X-Cybozu-API-Token": api_token, "Content-Type": "application/json"}

# name_name = input("名前を入力してください：")
# tel_name = input("電話番号を入力してください：")
# email_name = input("Emailを入力してください：")


def my_app2():
    name_name = name_entry.get()
    tel_name = tel_entry.get()
    email_name = email_entry.get()

    data = {
        "app": app_id,
        "record": {
            "name": {"value": name_name},
            "tel": {"value": tel_name},
            "email": {"value": email_name},
        },
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:  # 200が正常の応答
        print("データが正常に追加されました")
    else:
        print("エラーが発生しました", response.status_code)


root = tkinter.Tk()
root.title("my_app2")


Label(root, text="あなたの名前を入力してください。", font=("Arial", 16)).pack(padx=20, pady=10)

name_entry = Entry(root, font=("Arial", 14))
name_entry.pack(padx=20, pady=10)

Label(root, text="あなたの電話番号を入力してください", font=("Arial", 16)).pack(padx=20, pady=10)

tel_entry = Entry(root, font=("Arial", 14))
tel_entry.pack(padx=20, pady=10)

Label(root, text="あなたのEmailを入力してください", font=("Arial", 16)).pack(padx=20, pady=10)

email_entry = Entry(root, font=("Arial", 14))
email_entry.pack(padx=20, pady=10)

Button(root, text="送信", font=("Arial", 14), command=my_app2).pack(padx=20, pady=10)

root.mainloop()
