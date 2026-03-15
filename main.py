from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import engine, SessionLocal
import models
from models import Post

models.Base.metadata.create_all(bind=engine)


# 取得 db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PostCreate(BaseModel):
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
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts


@app.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="找不到這篇文章")
    return post


@app.post("/posts")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = Post(title=post.title, body=post.body, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# PUT /posts/{post_id} - 修改文章
@app.put("/posts/{post_id}")
def update_post(post_id: int, post: PostCreate, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="找不到這篇文章")
    db_post.title = post.title
    db_post.body = post.body
    db_post.published = post.published
    db.commit()
    db.refresh(db_post)
    return db_post


# DELETE /posts/{post_id} - 刪除文章
@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="找不到這篇文章")
    db.delete(post)
    db.commit()
    return {"message": "刪除成功"}


@app.get("/items/{item_id}")
def get_items(item_id: int, limit: int, skip: int = 0, keyword: str | None = None):
    return {"id": item_id, "limit": limit, "skip": skip, "keyword": keyword}
