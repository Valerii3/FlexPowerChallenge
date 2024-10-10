import argparse
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from src.task3.parser import get_yesterday, parse_arguments
from src.task3.statistics_calculator import process_trades


class TestGetYesterday(unittest.TestCase):
    def test_get_yesterday(self):
        expected_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.assertEqual(get_yesterday(), expected_date)


class TestParseArguments(unittest.TestCase):

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(trader_id='trader1', start_day=get_yesterday(), end_day=None))
    def test_defaults(self, mock_args):
        # Test case when no start_day and end_day are provided
        args = parse_arguments()
        expected_yesterday = get_yesterday()

        self.assertEqual(args.start_day, expected_yesterday)
        self.assertEqual(args.end_day, expected_yesterday)
        self.assertEqual(args.trader_id, 'trader1')

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(trader_id='trader1', start_day='2024-10-01', end_day=None))
    def test_start_day_provided(self, mock_args):
        # Test case when only start_day is provided, and end_day should default to start_day
        args = parse_arguments()
        self.assertEqual(args.start_day, '2024-10-01')
        self.assertEqual(args.end_day, '2024-10-01')
        self.assertEqual(args.trader_id, 'trader1')

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(trader_id='trader1', start_day='2024-10-01', end_day='2024-10-05'))
    def test_valid_dates_provided(self, mock_args):
        # Test case when both start_day and end_day are provided
        args = parse_arguments()
        self.assertEqual(args.start_day, '2024-10-01')
        self.assertEqual(args.end_day, '2024-10-05')
        self.assertEqual(args.trader_id, 'trader1')

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(trader_id='trader1', start_day='2024-10-05', end_day='2024-10-01'))
    def test_invalid_date_range(self, mock_args):
        # Test case when end_day is earlier than start_day
        with self.assertRaises(SystemExit):
            parse_arguments()

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(trader_id='trader1', start_day='invalid-date', end_day=None))
    def test_invalid_date_format(self, mock_args):
        # Test case with invalid date format
        with self.assertRaises(SystemExit):
            parse_arguments()


class TestProcessTrades(unittest.TestCase):

    def test_empty_trades(self):
        # Test case with no trades
        trades_for_current_date = []
        trades_by_hour, statistics = process_trades(trades_for_current_date)

        self.assertEqual(len(trades_by_hour), 0)
        self.assertEqual(statistics.num_trades, 0)
        self.assertEqual(statistics.num_buy, 0)
        self.assertEqual(statistics.num_sell, 0)
        self.assertEqual(statistics.pnl, 0.0)

    def test_single_trade(self):
        # Test case with one trade
        trades_for_current_date = [
            {
                'execution_time': '2024-10-10T14:30:00',
                'direction': 'buy',
                'quantity': 10,
                'price': 100
            }
        ]
        trades_by_hour, statistics = process_trades(trades_for_current_date)

        # Check trades for hour 14-15
        self.assertIn(14, trades_by_hour)
        self.assertEqual(trades_by_hour[14].num_trades, 1)
        self.assertEqual(trades_by_hour[14].num_buy, 10)
        self.assertEqual(trades_by_hour[14].num_sell, 0)
        self.assertEqual(trades_by_hour[14].pnl, -1000)  # 10 * -100

        # Check total statistics
        self.assertEqual(statistics.num_trades, 1)
        self.assertEqual(statistics.num_buy, 10)
        self.assertEqual(statistics.num_sell, 0)
        self.assertEqual(statistics.pnl, -1000)

    def test_multiple_trades_same_hour(self):
        # Test case with multiple trades in the same hour
        trades_for_current_date = [
            {
                'execution_time': '2024-10-10T14:30:00',
                'direction': 'buy',
                'quantity': 10,
                'price': 100
            },
            {
                'execution_time': '2024-10-10T14:45:00',
                'direction': 'sell',
                'quantity': 5,
                'price': 150
            }
        ]
        trades_by_hour, statistics = process_trades(trades_for_current_date)

        # Check trades for hour 14-15
        self.assertIn(14, trades_by_hour)
        self.assertEqual(trades_by_hour[14].num_trades, 2)
        self.assertEqual(trades_by_hour[14].num_buy, 10)
        self.assertEqual(trades_by_hour[14].num_sell, 5)
        self.assertEqual(trades_by_hour[14].pnl, -250)

        # Check total statistics
        self.assertEqual(statistics.num_trades, 2)
        self.assertEqual(statistics.num_buy, 10)
        self.assertEqual(statistics.num_sell, 5)
        self.assertEqual(statistics.pnl, -250)

    def test_multiple_trades_different_hours(self):
        # Test case with multiple trades in different hours
        trades_for_current_date = [
            {
                'execution_time': '2024-10-10T14:30:00',
                'direction': 'buy',
                'quantity': 10,
                'price': 100
            },
            {
                'execution_time': '2024-10-10T15:30:00',
                'direction': 'sell',
                'quantity': 5,
                'price': 150
            }
        ]
        trades_by_hour, statistics = process_trades(trades_for_current_date)

        # Check trades for hour 14-15
        self.assertIn(14, trades_by_hour)
        self.assertEqual(trades_by_hour[14].num_trades, 1)
        self.assertEqual(trades_by_hour[14].num_buy, 10)
        self.assertEqual(trades_by_hour[14].num_sell, 0)
        self.assertEqual(trades_by_hour[14].pnl, -1000)

        # Check trades for hour 15-16
        self.assertIn(15, trades_by_hour)
        self.assertEqual(trades_by_hour[15].num_trades, 1)
        self.assertEqual(trades_by_hour[15].num_buy, 0)
        self.assertEqual(trades_by_hour[15].num_sell, 5)
        self.assertEqual(trades_by_hour[15].pnl, 750)

        # Check total statistics
        self.assertEqual(statistics.num_trades, 2)
        self.assertEqual(statistics.num_buy, 10)
        self.assertEqual(statistics.num_sell, 5)
        self.assertEqual(statistics.pnl, -250)


if __name__ == "__main__":
    unittest.main()