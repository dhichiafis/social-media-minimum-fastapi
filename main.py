from fastapi import FastAPI
import uvicorn
from router import profile,users,post,comment
from database import Base,engine


app=FastAPI(title="a Simple social media clone",
        description='this is a social media clone illustrating a simple crud operations and many to many relationships in the  database and the perfomance of such crud apps',
        version='1.0.0',
        servers=[{
            "url":'http://localhost:8000',
            "description":"Development server"
        }])
Base.metadata.create_all(bind=engine)
app.include_router(users.users_router)
app.include_router(profile.profile_router)
app.include_router(post.post_router)

app.include_router(comment.comments_router)

@app.get("/")
async def home():
    return {"message":'welcome to social media'}

if __name__=="__main__":
    uvicorn.run("main:app",reload=True,port=8000,host="127.0.0.1")