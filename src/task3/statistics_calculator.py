from datetime import datetime, timedelta
from src.task3.statistic import Statistic
from src.task3.utils import retrieve_trades


def process_trades(trades_for_current_date):
    trades_by_hour = {}
    statistics = Statistic("Total")

    # Process trades by hour
    for trade_data in trades_for_current_date:
        hour = datetime.strptime(
            trade_data['execution_time'], '%Y-%m-%dT%H:%M:%S').hour
        direction = trade_data['direction']
        quantity = trade_data['quantity']
        price = trade_data['price']

        if hour not in trades_by_hour:
            trades_by_hour[hour] = Statistic(
                current_hour=f"{hour}-{(hour + 1) % 24}")

        trade_obj = trades_by_hour[hour]
        trade_obj.num_trades += 1

        if direction == 'buy':
            trade_obj.num_buy += quantity
            trade_obj.pnl -= quantity * price
        else:
            trade_obj.num_sell += quantity
            trade_obj.pnl += quantity * price

    # Update total statistics
    for trade_obj in trades_by_hour.values():
        statistics.add(trade_obj)

    return trades_by_hour, statistics


def calculate_statistics(id: str, start_date: datetime.date = datetime.now() - timedelta(days=1), end_date: datetime.date = None):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    current_date = start_date
    combined_hourly_statistics = {}
    daily_statistics = {}
    total_hourly_stats = Statistic("Total")

    while current_date <= end_date:

        trades_for_current_date = retrieve_trades(id, current_date)

        trades_by_hour, daily_stats = process_trades(trades_for_current_date)
        daily_statistics[current_date.strftime('%Y-%m-%d')] = daily_stats
        total_hourly_stats.add(daily_stats)
        # Accumulate hourly stats into combined statistics
        for hour, trade_obj in trades_by_hour.items():
            if hour not in combined_hourly_statistics:
                combined_hourly_statistics[hour] = Statistic(
                    current_hour=f"{hour}-{(hour + 1) % 24}")
            combined_hourly_statistics[hour].add(trade_obj)

        current_date += timedelta(days=1)

    combined_hourly_statistics["Total"] = total_hourly_stats
    daily_statistics["Total"] = total_hourly_stats

    return combined_hourly_statistics, daily_statistics
