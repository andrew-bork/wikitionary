from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/term/{term}")
async def get_term(term:str):
    print(term)
    return {"message": "Hello World"}