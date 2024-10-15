from pydantic import BaseModel
from typing import List

class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    title: str
    body: str
    class Config():
        from_attributes = True


class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[BlogBase] =[]
    class Config():
        from_attributes = True

class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser
    class Config():
        from_attributes = True