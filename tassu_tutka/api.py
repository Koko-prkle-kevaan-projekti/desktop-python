import queue
from fastapi import FastAPI, APIRouter
import uvicorn


class ClientApi(APIRouter):
    """Encapsulates desktop facing api in one class.
    
    Includes and owns a queue for messages from GPS-facing socket server.
    """

    _app = FastAPI()
    _queue = queue.Queue()

    def __init__(self, options, *args, **kwargs):
        """Initialize ClientApi

        Args:
            options (_type_): Options from argparse
            args and kwargs : Pass directly to APIRouter
        """
        super().__init__(*args, **kwargs)
        self.options = options

        # Add api route
        self.add_api_route("/get_lines", self.read_items)

        # Add router to the app instance.
        self._app.include_router(self)


    def push_to_queue(self, item: str):
        self._queue.put(item)
    
    def _pop_from_queue(self) -> str:
        return self._queue.get_nowait()
    
    def _queue_is_empty(self) -> bool:
        return self._queue.empty()

    def read_items(self) -> dict[str, list[str]]:
        lines = []
        while not self._queue_is_empty():
            lines.append(self._pop_from_queue())
        return {"lines": lines}

    def run_forevaa(self):
        """Serve"""
        uvicorn.run(
            self._app,
            host=self.options.api_addr,
            port=int(self.options.api_port),
            workers=0,
            loop="none",
            log_config=None,
        )
