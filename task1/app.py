import os
from datetime import datetime

from flask import Flask, jsonify, request

from extensions import db, ma
from task1.models import Trade, trades_schema
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

USER_DATA = {
    "Username": "Password"
}

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'trades.db')

db.init_app(app)
ma.init_app(app)


@app.route('/v1/trades', methods=['GET'])
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


@app.route('/v1/trades', methods=['POST'])
@auth.login_required
def post_trade():
    trade_data = request.json

    try:
        new_trade = Trade(
            id=trade_data['id'],
            price=trade_data['price'],
            quantity=trade_data['quantity'],
            direction=trade_data['direction'],
            delivery_day=trade_data['delivery_day'],
            delivery_hour=trade_data['delivery_hour'],
            trader_id=trade_data['trader_id'],
            execution_time=trade_data['execution_time']
        )
        db.session.add(new_trade)
        db.session.commit()
        return jsonify({'status_code': 200, 'message': 'Trade successfully added'}), 200
    except Exception as e:
        return jsonify({'status_code': 400, 'message': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)