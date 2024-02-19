from typing import List

from pydantic import BaseModel


class ToDoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool

    # pydantic 에서 sqlalchemy를 바로 읽어줄 수 있는 옵션
    # 위의 ToDoSchema의 sqlalchemy orm객체를 던져주게 되면 pydantic이 자동으로 읽어준다
    class Config:
        orm_mode = True

class ListToDoResponse(BaseModel):
    todos: List[ToDoSchema]

