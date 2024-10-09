
from sqlalchemy import Column, Integer, String, DateTime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow, Schema, fields, validate
from extensions import db, ma



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
    class Meta:
        fields = ('id', 'price', 'quantity', 'direction', 'delivery_day', 'delivery_hour', 'trader_id', 'execution_time')



trade_schema = TradeSchema()
trades_schema = TradeSchema(many=True)
