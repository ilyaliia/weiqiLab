from fastapi import FastAPI
from api import auth
from api import books

app = FastAPI()

app.include_router(auth.router)
app.include_router(books.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
