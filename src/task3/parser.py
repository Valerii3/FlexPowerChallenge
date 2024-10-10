import argparse
from datetime import datetime, timedelta


def get_yesterday():
    return (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Process trades for a specific trader within a date range.")

    # Required argument for trader_id
    parser.add_argument('trader_id', type=str, help="ID of the trader")

    # Optional argument for start_day (default is yesterday)
    parser.add_argument('--start_day', type=str, default=get_yesterday(),
                        help="Start day for the trade query (format: YYYY-MM-DD). Defaults to yesterday.")

    # Optional argument for end_day (default is the same as start_day)
    parser.add_argument('--end_day', type=str,
                        help="End day for the trade query (format: YYYY-MM-DD). Defaults to start_day.")

    args = parser.parse_args()

    # If end_day is not provided, set it to start_day
    if not args.end_day:
        args.end_day = args.start_day

    try:
        start_date = datetime.strptime(args.start_day, '%Y-%m-%d')
        end_date = datetime.strptime(args.end_day, '%Y-%m-%d')
    except ValueError as e:
        parser.error(f"Invalid date format: {e}")

    if end_date < start_date:
        parser.error("End day cannot be earlier than the start day.")

    return args
