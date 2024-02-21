from typing import List

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from db.orm import ToDo


def get_todos(session: Session) -> List[ToDo]:
    return list(session.scalars(select(ToDo)))


def get_todo_by_todo_id(session: Session, todo_id: int) -> ToDo | None:
    return session.scalar(select(ToDo).where(ToDo.id == todo_id))


def create_todo(session: Session, todo: ToDo) -> ToDo:
    session.add(instance=todo)
    session.commit() # db 저장
    session.refresh(instance=todo) # db read -> todo_id값 결정
    return todo

def update_todo(session: Session, todo: ToDo) -> ToDo:
    session.add(instance=todo)
    session.commit()
    session.refresh(instance=todo)
    return todo

def delete_todo(session: Session, todo_id: ToDo) -> None:
    session.execute(delete(ToDo).where(ToDo.id == todo_id))
    session.commit()
