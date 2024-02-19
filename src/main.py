from typing import List

from fastapi import FastAPI, Body, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.connection import get_db
from db.orm import ToDo
from db.repository import get_todos
from schema.response import ListToDoResponse, ToDoSchema


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
    ) -> ListToDoResponse:

    todos: List[ToDo] = get_todos(session=session)
    
    if order and order == "desc":
        return ListToDoResponse(
        todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]]
        )
    return ListToDoResponse(
        todos=[ToDoSchema.from_orm(todo) for todo in todos]
    )


@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(todo_id: int):
    todo = todo_data.get(todo_id)
    if todo:
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")


class CreateToDoRequest(BaseModel):
    id: int
    contents: str
    is_done: bool

@app.post("/todos", status_code=201)
def create_todo_handler(request: CreateToDoRequest):
    todo_data[request.id] = request
    return todo_data[request.id]


@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(todo_id: int, is_done: bool = Body(..., embed=True)):
    todo = todo_data.get(todo_id)
    if todo:
        todo["is_done"] = is_done
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(todo_id: int):
    todo = todo_data.pop(todo_id, None)
    if todo:
        return
    raise HTTPException(status_code=404, detail="Todo not found")