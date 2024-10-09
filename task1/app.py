from datetime import datetime

from flask import Flask, jsonify, request
from sqlalchemy import SQLAlchemy

from task1.models import Trade, trades_schema

app = Flask(__name__)


@app.route('/v1/trades', methods=['GET'])
def get_trades():
    trader_id = request.args.get('trader_id')
    delivery_day = request.args.get('delivery_day')

    try:
        query = Trade.query

        if trader_id:
            query = query.filter_by(trader_id=trader_id)
        if delivery_day:
            delivery_day_date = datetime.strptime(delivery_day, '%Y-%m-%d').date()
            query = query.filter_by(delivery_day=delivery_day_date)

        trades = query.all()
        return trades_schema.jsonify(trades), 200
    except Exception as e:
        return jsonify({'status_code': 400, 'message': str(e)}), 400


