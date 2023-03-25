from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/get_lines")
def read_item() -> dict[str, list[str]]:
    lines = []
    while not gps_events.empty() :
        lines.append(gps_events.get_nowait())
    return {"lines": lines}


def run(options):
    uvicorn.run(
        app,
        host=options.api_addr,
        port=int(options.api_port),
        workers=0,
        loop="none",
        log_config=None,
    )
