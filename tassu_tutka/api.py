from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, Field

from tassu_tutka.server import BUF, BUF_LOCK


app = FastAPI()


@app.get("/get_lines")
def read_item() -> dict[str, list[str]]:
    lines = []
    while line := readline():
        lines.append(line)
    return {"lines": lines}


def readline() -> str | None:
    """Return a line from BUF

    Reads a line from the BUF, to which the server facing GPS device writes to.
    The function will return None if BUF doesn't have a full line.
    """
    global BUF
    line = ""
    BUF_LOCK.acquire(blocking=True)
    for i, ch in enumerate(BUF):
        line += ch
        if ch == "\n":
            BUF = BUF[i + 1 :]
            break
    else:  # A full line in buffer isn't available.
        BUF_LOCK.release()
        return None
    BUF_LOCK.release()
    return line


def run():
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=0, loop="none")
