from sqlalchemy import Column, Integer, String, DateTime, Date
from flask_marshmallow import Schema
from src.task1.extensions import db


class Trade(db.Model):
    __tablename__ = 'trade'

    id = Column(String, primary_key=True)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    direction = Column(String, nullable=False)
    delivery_day = Column(Date, nullable=False, index=True)
    delivery_hour = Column(Integer, nullable=False)
    trader_id = Column(String, nullable=False, index=True)
    execution_time = Column(DateTime, nullable=False)


class TradeSchema(Schema):
    class Meta:
        fields = ('id', 'price', 'quantity', 'direction', 'delivery_day', 'delivery_hour', 'trader_id', 'execution_time')


trade_schema = TradeSchema()
trades_schema = TradeSchema(many=True)
