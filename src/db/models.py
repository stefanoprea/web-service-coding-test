from sqlalchemy import Column, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class KPI(Base):
    __tablename__ = "kpis"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("kpis.id", ondelete="CASCADE"))

    values = relationship(
        "Value",
        backref="kpis",
        cascade="all, delete",
        passive_deletes=True
        )


class Value(Base):
    __tablename__ = "vals"
    __table_args__ = (Index("idx_vals_on_kpi_id_and_date", "kpi_id", "date"),)

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    value = Column(String, nullable=False)
    kpi_id = Column(
        Integer,
        ForeignKey("kpis.id", ondelete="CASCADE"),
        nullable=False
        )
