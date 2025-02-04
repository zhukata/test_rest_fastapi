from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/users")
def get_users():
    return "Hello world"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)