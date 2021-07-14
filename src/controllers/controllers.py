from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import controllers.schemas as schemas
import db.crud as crud
import db.models as models
from pydantic import NonNegativeInt


def App(db_connector):
    app = FastAPI()

    # Dependency
    get_db = db_connector.get_db

    @app.post(
        "/kpi/",
        status_code=201,
        response_model=schemas.KPI
        )
    def post_kpi(params: schemas.PostKPIParams, db: Session = Depends(get_db)):
        try:
            return crud.create_kpi(db, params)
        except crud.ForeignKeyError:
            raise HTTPException(status_code=422, detail="Wrong parent_id")

    @app.post(
        "/value/",
        status_code=201,
        response_model=schemas.Value
        )
    def post_value(params: schemas.PostValueParams, db: Session = Depends(get_db)):
        try:
            return crud.create_value(db, params)
        except crud.ForeignKeyError:
            raise HTTPException(status_code=422, detail="Bad kpi_id")

    @app.delete("/kpi/{id}")
    def delete_kpi(id: NonNegativeInt, db: Session = Depends(get_db)):
        deleted_count = crud.delete_kpi(db, id)
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="KPI not found")

    @app.get(
        "/kpi/{id}",
        response_model=schemas.KPIWithValues
        )
    def get_kpi_with_children(id: NonNegativeInt, db: Session = Depends(get_db)):
        kpi = crud.get_kpi_with_values(db, id=id)
        if kpi is None:
            raise HTTPException(status_code=404, detail="KPI not found")
        return kpi

    @app.get(
        "/value/{id}",
        response_model=schemas.Value
        )
    def get_value(id: NonNegativeInt, db: Session = Depends(get_db)):
        value = crud.get_value(db, id=id)
        if value is None:
            raise HTTPException(status_code=404, detail="Value not found")
        return value

    return app
