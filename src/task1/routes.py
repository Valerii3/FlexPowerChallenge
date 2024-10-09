from flask import Blueprint, request, jsonify
from datetime import datetime
from src.task1.extensions import db
from src.task1.models import Trade, trades_schema
from src.task1.auth import auth
import re

trade_bp = Blueprint('trade_bp', __name__)


def validate_direction(direction):
    pattern = r'^(buy|sell)$'
    return re.match(pattern, direction)


@trade_bp.route('/trades', methods=['GET'])
@auth.login_required
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


@trade_bp.route('/trades', methods=['POST'])
@auth.login_required
def post_trade():
    trade_data = request.json
    direction = trade_data.get('direction', None)

    if not direction or not validate_direction(direction):
        return jsonify({'status_code': 400, 'message': 'Invalid direction. Must be "buy" or "sell".'}), 400

    try:
        new_trade = Trade(
            id=trade_data['id'],
            price=trade_data['price'],
            quantity=trade_data['quantity'],
            direction=trade_data['direction'],
            delivery_day=datetime.strptime(trade_data['delivery_day'], '%Y-%m-%d').date(),
            delivery_hour=trade_data['delivery_hour'],
            trader_id=trade_data['trader_id'],
            execution_time=datetime.strptime(trade_data['execution_time'], '%Y-%m-%dT%H:%M:%S')
        )

        db.session.add(new_trade)
        db.session.commit()
        return jsonify({'status_code': 200, 'message': 'Trade successfully added'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status_code': 400, 'message': str(e)}), 400
