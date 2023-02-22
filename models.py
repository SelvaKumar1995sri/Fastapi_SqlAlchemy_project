from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from datetime import datetime
from pytz import timezone

from db import Base
    
class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True,index=True)
    product = Column(String(100), nullable=False,index=True)
    seller = Column(String(80),nullable=False,index=True)
    price = Column(Float(precision=2), nullable=False)
    date = Column(DateTime(timezone=True), default=datetime.now().date())
    location = Column(String(200))
    categories = Column(String(200))
    
    
#date = Column(String(10),nullable=False)
#DateTime(timezone=True), default=datetime.now().date()
    #json_str = excel_data_df.to_json(orient="records")
    #print('Excel Sheet to JSON:\n', json_str)
    #d = json.loads(json_str)
    #print(excel_data_df.head())