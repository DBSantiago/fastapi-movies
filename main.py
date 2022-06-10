from fastapi import FastAPI

app = FastAPI(title="Movies Reviews", description="A project where we can review movies", version="1")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
