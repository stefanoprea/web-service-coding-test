from typing import List, Optional
from pydantic import BaseModel, NonNegativeInt, validator
import datetime


class PostValueParams(BaseModel):
    date: str
    value: str
    kpi_id: NonNegativeInt

    @validator("date")
    def validate_date(cls, v):
        try:
            datetime.datetime.strptime(v, "%Y-%m-%d")
        except ValueError as e:
            raise e
        return v


class Value(BaseModel):
    id: int
    date: str
    value: str
    kpi_id: NonNegativeInt

    class Config:
        orm_mode = True


class ChildValue(BaseModel):
    date: str
    value: str

    class Config:
        orm_mode = True
        

class KPIBase(BaseModel):
    name: str
    description: str
    parent_id: Optional[NonNegativeInt] = None


class PostKPIParams(KPIBase):
    pass


class KPI(KPIBase):
    id: int

    class Config:
        orm_mode = True


class KPIWithValues(KPI):
    values: List[ChildValue]

    class Config:
        orm_mode = True
