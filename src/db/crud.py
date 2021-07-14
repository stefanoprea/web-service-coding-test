from sqlalchemy.orm import Session
from sqlalchemy import exc
import controllers.schemas as schemas
import db.models as models
from pydantic import NonNegativeInt


class ForeignKeyError(Exception):
    @classmethod
    def decorate(cls, function):
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except exc.IntegrityError as e:
                if "foreign key".casefold() in str(e).casefold():
                    raise cls()
                raise e
        return wrapper

@ForeignKeyError.decorate
def create_kpi(db: Session, request_params: schemas.PostKPIParams):
    params = {
        "name": request_params.name,
        "description": request_params.description
    }
    parent_id = request_params.parent_id
    if isinstance(parent_id, int):
        params["parent_id"] = request_params.parent_id
    db_item = models.KPI(**params)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@ForeignKeyError.decorate
def create_value(db: Session, request_params: schemas.PostValueParams):
    db_item = models.Value(**request_params.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_kpi_with_values(db: Session, id: NonNegativeInt):
    kpi = db.query(models.KPI).filter(models.KPI.id == id).first()
    values = (
        db
        .query(models.Value)
        .filter(models.Value.kpi_id == id)
        .order_by(models.Value.date.desc())
        .limit(5)
        .all()
        )
    if kpi:
        kpi.values = values
    return kpi

def get_value(db: Session, id: NonNegativeInt):
    return db.query(models.Value).filter(models.Value.id == id).first()

def delete_kpi(db: Session, id: NonNegativeInt):
    deleted_count = db.query(models.KPI).filter(models.KPI.id == id).delete()
    db.commit()
    return deleted_count
