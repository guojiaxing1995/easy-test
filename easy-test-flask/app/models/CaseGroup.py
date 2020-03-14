from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, String


class CaseGroup(Base):

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=True, unique=True)
    info = Column(String(50))