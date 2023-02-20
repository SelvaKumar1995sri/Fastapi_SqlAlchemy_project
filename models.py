from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
import datetime
from pytz import timezone

from db import Base
    
class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True,index=True)
    product = Column(String(100), nullable=False, unique=True,index=True)
    seller = Column(String(80),nullable=False,index=True)
    price = Column(Float(precision=2), nullable=False)
    date = Column(DateTime(timezone=True), default=datetime.datetime.now(timezone('Asia/Kolkata')))
    location = Column(String(200))
    categories = Column(String(200))
    
    def __repr__(self):
        return 'ItemModel(name=%s, price=%s,store_id=%s)' % (self.name, self.price,self.store_id)
    
