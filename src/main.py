from typing import List

from fastapi import FastAPI, Body, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.connection import get_db
from db.orm import ToDo
from db.repository import create_todo, delete_todo, get_todo_by_todo_id, get_todos, update_todo
from schema.response import ToDoListSchema, ToDoSchema
from schema.request import CreateToDoRequest


app = FastAPI()

@app.get("/")
def health_check_hangler():
    return {"status": "OK"}


todo_data = {
    1: {
        "id": 1,
        "contents": "FastAPI",
        "is_done": True,
    },
    2: {
        "id": 2,
        "contents": "FastAPI 2",
        "is_done": False,
    },
    3: {
        "id": 3,
        "contents": "FastAPI 3",
        "is_done": False,
    }
}

@app.get("/todos", status_code=200)
def get_todos_handler(
        order: str | None = None,
        session: Session = Depends(get_db)
    ) -> ToDoListSchema:

    todos: List[ToDo] = get_todos(session=session)
    
    if order and order == "desc":
        return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]]
        )
    return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos]
    )


@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(
        todo_id: int,
        session: Session = Depends(get_db)
    ) -> ToDoSchema:
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Todo not found")


@app.post("/todos", status_code=201)
def create_todo_handler(
        request: CreateToDoRequest,
        session: Session = Depends(get_db)
    ) -> ToDoSchema:
    todo: ToDo = ToDo.create(request=request) # id=None
    todo: ToDo = create_todo(session=session, todo=todo) # id=int

    return ToDoSchema.from_orm(todo)


@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True),
        session: Session = Depends(get_db)
    ):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        # update
        todo.done() if is_done else todo.undone()
        todo: ToDo = update_todo(session=session, todo=todo)
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(
        todo_id: int,
        session: Session = Depends(get_db)
    ):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    delete_todo(session=session, todo_id=todo_id)
    