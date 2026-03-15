from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Post(BaseModel):
    title: str
    body: str
    published: bool = True


posts = [
    {"id": 1, "title": "第一篇文章", "body": "內容一", "published": True},
    {"id": 2, "title": "第二篇文章", "body": "內容二", "published": True},
    {"id": 3, "title": "第三篇文章", "body": "內容三", "published": True},
]


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}


@app.get("/posts")
def get_posts():
    return posts


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = next((p for p in posts if p["id"] == post_id), None)
    if post is None:
        raise HTTPException(status_code=404, detail="找不到這篇文章")
    return post


# POST /posts - 新增文章
@app.post("/posts")
def create_post(post: Post):
    new_id = max((p["id"] for p in posts), default=0) + 1
    new_post = {
        "id": new_id,
        "title": post.title,
        "body": post.body,
        "published": post.published,
    }
    posts.append(new_post)
    return {"message": "新增成功", "data": new_post}


# PUT /posts/{post_id} - 修改文章
@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    idx = next((i for i, p in enumerate(posts) if p["id"] == post_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="找不到這篇文章")
    posts[idx] = {
        "id": post_id,
        "title": post.title,
        "body": post.body,
        "published": post.published,
    }
    return {"message": "修改成功", "data": posts[idx]}


# DELETE /posts/{post_id} - 刪除文章
@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    idx = next((i for i, p in enumerate(posts) if p["id"] == post_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="找不到這篇文章")
    posts.pop(idx)
    return {"message": "刪除成功"}


@app.get("/items/{item_id}")
def get_items(item_id: int, limit: int, skip: int = 0, keyword: str | None = None):
    return {"id": item_id, "limit": limit, "skip": skip, "keyword": keyword}
