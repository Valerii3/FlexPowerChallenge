
from src.task3.statistics_calculator import calculate_statistics
from src.task3.parser import parse_arguments
from src.task3.utils import display_per_hour, display_daily_stats


def main():
    args = parse_arguments()
    hourly_stats, daily_stats = calculate_statistics(
        args.trader_id, args.start_day, args.end_day)

    if args.start_day == args.end_day:
        print(f"--- Hourly Stats for {args.trader_id} on {args.start_day}---")
        display_per_hour(hourly_stats)
    else:
        print("--- Hourly Stats for each day ---")
        display_per_hour(hourly_stats)
        print("--- Daily Summary ---")
        display_daily_stats(daily_stats)


if __name__ == "__main__":
    main()
