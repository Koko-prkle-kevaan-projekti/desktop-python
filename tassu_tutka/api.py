from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/items/")
async def read_item():
    return "moro"

def run():
    uvicorn.run(app, host="0.0.0.0", port=8000)
    