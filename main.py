from fastapi import FastAPI
from api import auth, game, books, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(game.router)
app.include_router(users.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
