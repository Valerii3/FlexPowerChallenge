import os
import time
from datetime import datetime, timedelta
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

current_dir = os.path.dirname(os.path.abspath(__file__))

PATH = os.path.join(current_dir, "../resources/")
API_URL = "http://localhost:5000/v1/trades"

# It's better to store in some config file or environment variable, but for simplicity I will keep it here
USERNAME = "Admin"
PASSWORD = "Password"


def check_for_new_file():
    today = datetime.now() - timedelta(days=1)
    file_name = f"epex_trades_{today.strftime('%Y%m%d')}.csv"
    file_path = os.path.join(PATH, file_name)

    if os.path.exists(file_path):
        return file_path
    return None


def upload_trades(file_path):

    try:
        trades_df = pd.read_csv(file_path)

        for _, row in trades_df.iterrows():
            execution_time = datetime.strptime(
                row['execution_time'], '%Y-%m-%dT%H:%M:%SZ')
            trade_data = {
                'id': row['id'],
                'price': row['price'],
                'quantity': row['quantity'],
                'direction': row['direction'],
                'delivery_day': row['delivery_day'],
                'delivery_hour': row['delivery_hour'],
                'trader_id': row['trader_id'],
                'execution_time': execution_time.strftime('%Y-%m-%dT%H:%M:%S')
            }

            try:
                response = requests.post(
                    API_URL, json=trade_data, auth=HTTPBasicAuth(USERNAME, PASSWORD))

                if response.status_code == 201:
                    print(f"Successfully uploaded trade {row['id']}")
                else:
                    print(
                        f"Failed to upload trade {row['id']}, status code: {response.status_code}")
                    print(f"Response content: {response.text}")

            except requests.exceptions.RequestException as req_err:
                print(f"Request failed for trade {row['id']}: {req_err}")

    except Exception as e:
        print(f"An error occurred while uploading trades: {str(e)}")


def notify_user():
    # some notification logic can be here
    print("Ooops, where are all our trades?")
    pass


def main():
    start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    # safety measure, if there was no file at 00:00
    end_time = start_time.replace(hour=8)

    while (datetime.now() < end_time):
        file_path = check_for_new_file()
        if file_path:
            upload_trades(file_path)
            return

        time.sleep(30 * 60)  # It will check every 30 minutes

    notify_user()


if __name__ == '__main__':
    """
    uncomment next line, and it will add trades to the database :)
        upload_trades(PATH + "epex_trades_20230220.csv")
    """
    main()
