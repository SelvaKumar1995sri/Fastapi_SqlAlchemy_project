from sqlalchemy.orm import Session
from sqlalchemy import extract
import models
import schemas


class ItemRepo:
    
 async def create(db: Session, item: schemas.ItemCreate):
        db_item = models.Item(
            product=item.product,
            seller=item.seller,
            price=item.price,
            location=item.location,
            categories=item.categories)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
 async def create_all(db: Session, item: schemas.product_list):
        db_item = schemas.list_serializer(item)
        db.add_all(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item


 def fetch_by_id(db: Session,_id):
     return db.query(models.Item).filter(models.Item.id == _id).first()

 def fetch_by_month(date: str,db: Session):
    return db.query(models.Item.date).filter( models.Item.date == date)
    #return db.query(models.Item).filter(models.Item.date== date).first()
 
 def fetch_by_name(db: Session,product):
     return db.query(models.Item).filter(models.Item.product == product).first()
 
 def fetch_all(db: Session, skip: int = 0, limit: int = 100):
     return db.query(models.Item).offset(skip).limit(limit).all()
 
 async def delete(db: Session,item_id):
     db_item= db.query(models.Item).filter_by(id=item_id).first()
     db.delete(db_item)
     db.commit()

#  async def delete_all(db: Session,skip: int = 0, limit: int = 100):
#      data = db.query(models.Item).filter(skip).limit(limit).all()
#      db.delete(data)
#      db.commit() 
     
 async def update(db: Session,item_data):
    updated_item = db.merge(item_data)
    db.commit()
    return updated_item
    
    
    
