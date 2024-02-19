from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.orm import ToDo


def get_todos(session: Session) -> List[ToDo]:
    return list(session.scalars(select(ToDo)))