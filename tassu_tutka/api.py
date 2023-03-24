import pathlib
import lock
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, Field


app = FastAPI()


@app.get("/get_lines")
def read_item() -> dict[str, list[str]]:
    buffer_file_path = pathlib.Path("/tmp/ttutka.tmp")
    lock.lock(buffer_file_path)
    with open(buffer_file_path, "r") as fh:
        lines = fh.readlines()
    with open(buffer_file_path, "w") as fh:
        pass
    lock.unlock(buffer_file_path)
    return {"lines": lines}


def run(options):
    uvicorn.run(
        app, host=options.api_addr, port=int(options.api_port), workers=0, loop="none"
    )
