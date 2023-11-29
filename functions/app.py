from fastapi import FastAPI

app = FastAPI()

@app.get("/get_data")
def read_root():
    return {"message": "Hello, this is your FastAPI backend!"}
