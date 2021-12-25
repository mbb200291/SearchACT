from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.sql.sqltypes import INTEGER
from sqlalchemy.sql.sqltypes import VARCHAR

from .database import Base


class Department(Base):

    __tablename__ = "department"

    id = Column(INTEGER, unique=True)
    name = Column(VARCHAR(255), nullable=False, unique=True, primary_key=True)
    abbreviation = Column(VARCHAR(255), nullable=False)
    active = Column(Boolean, nullable=False)

    def __init__(self, name, abbreviation, active):
        self.name = name
        self.abbreviation = abbreviation
        self.active = active

    def __repr__(self):
        return f"<Department(\
                {self.id},\
                {self.name}, \
                {self.abbreviation}, \
                {self.active} \
                )>"
