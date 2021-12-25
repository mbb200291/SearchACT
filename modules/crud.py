from typing import List

from pydantic import validate_arguments
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import max

from .database import get_database_session
from .database import get_engine
from .models import Base
from .models import Department
from .schemas import Department as DepartmentSchema


def create_default_schema():
    engine = get_engine()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@validate_arguments(config=dict(arbitrary_types_allowed=True))
def create_or_update_departments(
    db: Session, departments: List[DepartmentSchema]
) -> List[DepartmentSchema]:

    departments_dic = {
        department.name: (Department(**department.dict(exclude_defaults=True)))
        for department in departments
    }
    last_id = get_department_last_id(next(get_database_session()))

    def _gen(start):
        while True:
            start += 1
            yield start

    last_id_generator = _gen(0) if not last_id else _gen(last_id)

    ret = list(departments_dic.values())

    for department in (
        db.query(Department).filter(Department.name.in_(departments_dic.keys())).all()
    ):
        # if each is in db, do update
        department_to_be_update = departments_dic.pop(department.name)

        db.merge(department_to_be_update)

    for item in departments_dic.values():
        item.id = next(last_id_generator)

    # others which are not in db, do insert
    db.add_all(departments_dic.values())

    db.commit()

    # convert to pydantic models
    ret = list(DepartmentSchema.from_orm(department) for department in ret)

    return ret


def get_department_all(
    db: Session = next(get_database_session()),
) -> List[DepartmentSchema]:
    return db.query(Department).all()


def get_department_last_id(db: Session = next(get_database_session())) -> int:
    return db.query(max(Department.id)).scalar()


def get_department(db: Session, name: str):
    return db.query(Department).filter(name=name).all()
