from pydantic import BaseModel, constr, conlist


class PostCoord(BaseModel):
    x: int
    y: int
    c: constr(min_length=1, max_length=1)


class PostArea(BaseModel):
    a: conlist(int, min_items=2, max_items=2)
    b: conlist(int, min_items=2, max_items=2)
