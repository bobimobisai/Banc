import uvicorn
from fastapi import FastAPI
from authentication.views import router as auth_router
from users.views import router as user_router

app = FastAPI(title="Banc")
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/")
def hello_index():
    return {"Welcome to the Banc body!!!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
