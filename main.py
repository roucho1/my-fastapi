from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
    {"id": 1, "title": "第一篇文章", "body": "內容一"},
    {"id": 2, "title": "第二篇文章", "body": "內容二"},
    {"id": 3, "title": "第三篇文章", "body": "內容三"},
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
    return {"message": "新增成功", "data": post}


@app.get("/items/{item_id}")
def get_items(item_id: int, limit: int, skip: int = 0, keyword: str | None = None):
    return {"id": item_id, "limit": limit, "skip": skip, "keyword": keyword}
