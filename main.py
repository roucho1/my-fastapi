from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}


@app.get("/posts")
def get_posts():
    return [
        {"id": 1, "title": "第一篇文章", "body": "內容一"},
        {"id": 2, "title": "第二篇文章", "body": "內容二"},
        {"id": 3, "title": "第三篇文章", "body": "內容三"},
    ]


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    return {"id": post_id, "title": f"第 {post_id} 篇文章", "body": "文章內容"}


# POST /posts - 新增文章
@app.post("/posts")
def create_post(post: dict):
    return {"message": "新增成功", "data": post}
