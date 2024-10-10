from prettytable import PrettyTable
from requests.auth import HTTPBasicAuth
from colorama import Fore, Style, init
import requests

from src.task1.config import API_URL
from src.task2.listener import USERNAME, PASSWORD


def make_colourful(pnl):

    init()
    if pnl > 0:
        pnl_per_hour = f"{Fore.GREEN}{pnl:.2f}{Style.RESET_ALL}"
    elif pnl < 0:
        pnl_per_hour = f"{Fore.RED}{pnl:.2f}{Style.RESET_ALL}"
    else:
        pnl_per_hour = f"{pnl:.2f}"
    return pnl_per_hour


def display_per_hour(trades_per_hour):

    sorted_trades = {k: trades_per_hour[k] for k in sorted(
        k for k in trades_per_hour.keys() if isinstance(k, int))}
    table = PrettyTable(
        ['Hour', 'Number of trade', 'Total Buy [MW]', 'Total Sell [MW]', 'PnL [Eur]'])
    sorted_trades["Total"] = trades_per_hour["Total"]

    for _, trades in sorted_trades.items():
        pnl_per_hour = make_colourful(trades.pnl)

        row = [f'{trades.current_hour}', f"{trades.num_trades}", f"{trades.num_buy}", f"{trades.num_sell}",
               pnl_per_hour]
        table.add_row(row)

    print(table)


def display_daily_stats(daily_statistics):
    table = PrettyTable(
        ['Day', 'Number of Trades', 'Total Buy [MW]', 'Total Sell [MW]', 'PnL [Eur]'])

    # Sort the daily statistics and add to table
    for day, stats in sorted(daily_statistics.items()):
        pnl_total = make_colourful(stats.pnl)
        row = [day, f"{stats.num_trades}", f"{stats.num_buy}",
               f"{stats.num_sell}", pnl_total]
        table.add_row(row)

    print(table)


def retrieve_trades(trader_id, current_date):
    delivery_day = current_date.strftime('%Y-%m-%d')

    params = {
        'trader_id': trader_id,
        'delivery_day': delivery_day
    }
    try:
        response = requests.get(API_URL, params=params,
                                auth=HTTPBasicAuth(USERNAME, PASSWORD))
        if response.status_code == 200:
            try:
                # Attempt to parse the JSON response
                trades = response.json()
                return trades
            except ValueError as e:
                # Handle case where response is not valid JSON
                print(f"Failed to parse JSON for {delivery_day}: {e}")
                print(f"Response content: {response.text}")
                return None
        else:
            print(
                f"Failed to retrieve trades for {delivery_day}: HTTP {response.status_code}")
            print(f"Response content: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {delivery_day}: {e}")
        return None
