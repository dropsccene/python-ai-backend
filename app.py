from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def read():
    return {"status":"ok"}
