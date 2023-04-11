from asyncio import threads
import json
import re
from typing import Any
import os
import queue
import httpx
from threading import Thread, Lock

import tassu_tutka.nmea as nmea



def _counter():
    count = 0
    while True:
        yield count
        count += 1


class Requester:
    def __init__(self) -> None:
        self._threads: dict[int, Thread] = dict()
        self._responses: queue.Queue = queue.Queue()
        self._counter = _counter()

    def _mkrequest(self, request_num):
        """Return request number."""
        addr = os.getenv("SERVER_ADDR")
        port = os.getenv("SERVER_PORT")
        try:
            response = httpx.get(f"http://{addr}:{port}/get_lines")
            print(f"_mkrequest(): response: {response}")
        except httpx.ConnectError as e:
            print("Connection refused.")
            return
        try:
            json_ = json.loads(response.text)
            if json_["lines"]:
                self._responses.put(json_["lines"])
        except json.decoder.JSONDecodeError as e:
            self._responses.put(response.status_code)

    def mkrequest(self):
        """Make the request"""
        num = next(self._counter)
        t = Thread(target=self._mkrequest, args=(num,))
        t.start()
        self._threads[num] = t
        return num

    def get_responses(self) -> list[str | int]:
        """Get arrived responses from queue.

        Returns:
            list[str]: Lines of messages in the queue.
        """
        complete = []
        for num, t in self._threads.items():
            if t.is_alive():
                continue
            t.join()
            complete.append(num)
        for i in complete:
            del self._threads[i]

        ret = []
        while not self._responses.empty():
            val = self._responses.get()
            print(val)
            sentences = []
            for raw_sentence in val:
                try:
                    sentences.append(nmea.Sentence(raw_sentence))
                except nmea.UnknownSentence as e:
                    pass
            ret.extend(sentences)

        return ret
