import unittest

from flask import json
from src.task1.app import app
from src.task1.extensions import db


def get_trade_data(direction="buy"):
    """Helper to get trade data"""
    return {
        "id": "trade_001",
        "price": 250,
        "quantity": 15,
        "direction": direction,
        "delivery_day": "2024-10-10",
        "delivery_hour": 12,
        "trader_id": "TraderA",
        "execution_time": "2024-10-09T14:30:00"
    }


def get_headers(auth=True):
    """Helper to create headers, including Authorization if needed."""
    if auth:
        return {"Authorization": "Basic VXNlcm5hbWU6UGFzc3dvcmQ=", "Content-Type": "application/json"} # hashed
    return {"Content-Type": "application/json"}


class TradeApiTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def post_trade(self, trade_data, auth=True):
        """Helper to post trade data."""
        return self.client.post('/v1/trades', data=json.dumps(trade_data),
                                headers=get_headers(auth=auth))

    def test_unauthenticated_post_request(self):
        """Test that an unauthenticated request is rejected"""
        trade_data = get_trade_data()
        response = self.post_trade(trade_data, auth=False)

        self.assertEqual(401, response.status_code)
        self.assertIn(b"Unauthorized", response.data)

    def test_unauthenticated_get_request(self):
        """Test that an unauthenticated GET request is rejected"""
        response = self.client.get('/v1/trades?trader_id=Trader1&delivery_day=2024-10-10')

        self.assertEqual(401, response.status_code)
        self.assertIn(b"Unauthorized", response.data)

    def test_successful_add_trade(self):
        """Test that a new trade is successfully added via POST."""
        trade_data = get_trade_data()
        response = self.post_trade(trade_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Trade successfully added", response.data)

    def test_successful_get_trade(self):
        """Test that an added trade is successfully retrieved via GET."""
        trade_data = get_trade_data(direction="sell")
        self.post_trade(trade_data)

        response = self.client.get('/v1/trades?trader_id=TraderA', headers=get_headers())

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"trade_001", response.data)

    def test_invalid_direction(self):
        """Test that trade with an invalid direction is rejected."""
        trade_data = get_trade_data(direction="borrow")
        response = self.post_trade(trade_data)

        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid direction', response.data)


if __name__ == '__main__':
    unittest.main()
