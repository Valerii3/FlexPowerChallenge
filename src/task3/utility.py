import argparse
from datetime import datetime, timedelta

from requests.auth import HTTPBasicAuth

from src.task1.config import API_URL
import requests

from src.task2.listener import USERNAME, PASSWORD


def get_yesterday():
    return (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')


def parse_arguments():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description="Process trades for a specific trader within a date range.")

    # Required argument for trader_id
    parser.add_argument('trader_id', type=str, help="ID of the trader")

    # Optional argument for start_day (default is yesterday)
    parser.add_argument('--start_day', type=str, default=get_yesterday(),
                        help="Start day for the trade query (format: YYYY-MM-DD). Defaults to yesterday.")

    # Optional argument for end_day (default is the same as start_day)
    parser.add_argument('--end_day', type=str,
                        help="End day for the trade query (format: YYYY-MM-DD). Defaults to start_day.")

    # Parse arguments
    args = parser.parse_args()

    # If end_day is not provided, set it to start_day
    if not args.end_day:
        args.end_day = args.start_day

    return args

def retrieve_trades(trader_id, current_date):
    delivery_day = current_date.strftime('%Y-%m-%d')

    params = {
        'trader_id': trader_id,
        'delivery_day': delivery_day
    }
    try:
        response = requests.get(API_URL, params=params,  auth=HTTPBasicAuth(USERNAME, PASSWORD))
        trades = response.json()
        return trades
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {delivery_day}: {e}")