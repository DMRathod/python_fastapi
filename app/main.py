from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import posts, users, auth, votes
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.config import settings
from app.database import create_database_and_tables, drop_database_and_tables, close_connection
from .model import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    # app.state.db = drop_database_and_tables()
    app.state.db = create_database_and_tables()
    print(app.state.db)

    yield

    app.state.db = close_connection()    
    print(app.state.db)


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(posts.router, prefix="/uposts", tags=["uposts"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(votes.router, prefix="/vote", tags=["votes"])



@app.get("/")
def root():
    return {"Message": "Welcome to FastAPI, My First Web APP"}


if __name__ == "__main__":
    port = settings.database_port
    uvicorn.run(app, host="0.0.0.0", port=port)


# class Post(BaseModel):
#     tittle: str
#     content: str
#     published: bool = True

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi', user='postgres', password='root', cursor_factory=RealDictCursor) 
#         cursor = conn.cursor()
#         print("Connected to Database")
#         break
#     except Exception as er:
#         print("Connection Failed")
#         print("Error: ", er)
#         time.sleep(3)   

# my_post = [{"tittle":"tittle of the post", "content":"content of the post", "id":1},
#            {"tittle":"tittle of the post", "content":"content of the post", "id":2}
# ]
# @app.get('/')
# def root():
#     return "Hello User"

# @app.post('/schema')
# def create_schema():
#     create_database_and_table()
#     return {"Tables Created"}

# @app.get('/posts')
# def get_list_of_all_post():
#     cursor.execute("SELECT * from posts")
#     posts = cursor.fetchall()
#     return {"data":posts}

# @app.post('/posts', status_code=status.HTTP_201_CREATED)
# def create_post(post: Post):
#     print(post.model_dump())
#     cursor.execute("INSERT INTO posts(tittle, content, published) VALUES (%s, %s, %s) RETURNING *",(post.tittle, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"message": new_post}

# @app.get('/posts/{id}')
# def get_post(id: int, response: Response):
#     print()
#     cursor.execute("SELECT * from posts WHERE id = %s", (id,))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with {id} not found")
#     return {"Message":f"This is your post with {id}", "post":post}

# @app.delete('/posts/delete/{id}')
# def delete_post(id: int):
#     cursor.execute("DELETE from posts where id = %s returning *", (str(id)))
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if not deleted_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"post with {id} not found")
#     return {"message": f"post with {id} deleted", "post": deleted_post}

# @app.put('/posts/update/{id}')
# def update_post(id: int, post: Post):
#     cursor.execute("update posts set tittle = %s, content = %s, published = %s where id = %s returning *", (str(post.tittle), post.content, post.published,str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()
    
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
#     return {"data": updated_post}

