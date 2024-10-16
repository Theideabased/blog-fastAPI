from fastapi import FastAPI
from blog_fastAPI import models
from blog_fastAPI.database import engine
from blog_fastAPI.routers import blog, user, authentication

app = FastAPI()


models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)