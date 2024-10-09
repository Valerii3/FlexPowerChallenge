from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from marshmallow import Schema, fields, validate
from flask_marshmallow import Marshmallow

from app import app

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Trade(db.Model):
    __tablename__ = 'trade'

    id = Column(String, primary_key=True)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    direction = Column(String, nullable=False)
    delivery_day = Column(DateTime, nullable=False)
    delivery_hour = Column(Integer, nullable=False)
    trader_id = Column(String, nullable=False)
    execution_time = Column(DateTime, default=datetime.utcnow)


class TradeSchema(Schema):
    id = fields.String(
        required=True, description="Unique id of the trade as defined by the exchange", example="trade_123")
    price = fields.Integer(
        required=True, description="Price in eurocent/MWh.", example=200)
    quantity = fields.Integer(
        required=True, description="Quantity in MW.", example=12)
    direction = fields.String(
        required=True,
        validate=validate.Regexp('^(buy|sell)$'),
        description="Direction of the trade from the perspective of flew-power, can be either buy or sell."
    )
    delivery_day = fields.Date(
        required=True, description="Day on which the energy has to be delivered in local time.")
    delivery_hour = fields.Integer(
        required=True, description="Hour during which the energy has to be delivered in local time.", example=14)
    trader_id = fields.String(
        required=True, description="Unique id of a trader (bot or team member).", example="MirkoT")
    execution_time = fields.DateTime(
        required=True, description="UTC datetime at which the trade occurred on the exchange.")


trade_schema = TradeSchema()
trades_schema = TradeSchema(many=True)
