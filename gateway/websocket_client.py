import json
from abc import ABC, abstractmethod


class WebsocketClient(ABC):
    _CONNECT_TIMEOUT_S = 5
    _ENDPOINT = 'wss://'

    @abstractmethod
    def send(self, message):
        pass

    def send_json(self, message):
        self.send(json.dumps(message))

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def reconnect(self) -> None:
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def on_message(self, message):
        pass

    @abstractmethod
    def on_close(self):
        pass
