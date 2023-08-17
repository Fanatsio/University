from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float, create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, Session

Base = declarative_base()

class Discipline(Base):
    __tablename__ = "discipline"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(25))
    lecture = Column(Integer)
    practice = Column(Integer)
    labs = Column(Integer)
    department_id = Column(Integer, ForeignKey("department.id"))
    type_of_control_id = Column(Integer, ForeignKey("type_of_control.id"))



class department(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(10))

    disciplines = relationship('Discipline', backref='department')


class Type_of_control(Base):
    __tablename__ = "type_of_control"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(15))

    disciplines = relationship('Discipline', backref='type_of_control')