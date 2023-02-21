from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
import models 
import pandas as pd
from db import get_db, engine
import models as models
import schemas as schemas
from repositories import ItemRepo
from sqlalchemy.orm import Session
import uvicorn
import json
from typing import List,Optional
from fastapi.encoders import jsonable_encoder

app = FastAPI(title="Sample FastAPI Application",
    description="Sample FastAPI Application with Swagger and Sqlalchemy",
    version="1.0.0",)

models.Base.metadata.create_all(bind=engine)

@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


@app.post("/upload")
async def upload_file( file: UploadFile = File(...) ):
    excel_data_df = pd.read_excel(file.file)
    excel_data_df.to_sql('items', con=engine, if_exists='append', index=False)
    return {"filename": file.filename}

@app.post("/export/{item_id}", tags=["Item"],response_model=schemas.Item)
async def export_file( file: UploadFile = File(...) ):
    excel_data_df = pd.read_excel(file.file)
    excel_data_df.to_sql('items', con=engine, if_exists='append', index=False)
    return {"filename": file.filename}

@app.post('/items', tags=["Item"],response_model=schemas.Item,status_code=201)
async def create_item(item_request: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = ItemRepo.fetch_by_name(db, product=item_request.product)
    if db_item:
        raise HTTPException(status_code=400, detail="Item already exists!")

    return await ItemRepo.create(db=db, item=item_request)

@app.get('/items', tags=["Item"],response_model=List[schemas.Item])
def get_all_items(db: Session = Depends(get_db)):
    return ItemRepo.fetch_all(db)


@app.get('/items/{item_id}', tags=["Item"],response_model=schemas.Item)
def get_item(item_id: int,db: Session = Depends(get_db)):
    db_item = ItemRepo.fetch_by_id(db,item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    return db_item


@app.delete('/items/{item_id}', tags=["Item"])
async def delete_item(item_id: int,db: Session = Depends(get_db)):
    db_item = ItemRepo.fetch_by_id(db,item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    await ItemRepo.delete(db,item_id)
    return "Item deleted successfully!"

@app.put('/items/{item_id}', tags=["Item"],response_model=schemas.Item)
async def update_item(item_id: int,item_request: schemas.Item, db: Session = Depends(get_db)):
    """
    Update an Item stored in the database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item:
        update_item_encoded = jsonable_encoder(item_request)
        db_item.product = update_item_encoded['product']
        db_item.seller = update_item_encoded['seller']
        db_item.price = update_item_encoded['price']
        db_item.date = update_item_encoded['date']
        db_item.location = update_item_encoded['location']
        db_item.categories = update_item_encoded['categories']
        return await ItemRepo.update(db=db, item_data=db_item)
    else:
        raise HTTPException(status_code=400, detail="Item not found with the given ID")
    
    


    

if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)