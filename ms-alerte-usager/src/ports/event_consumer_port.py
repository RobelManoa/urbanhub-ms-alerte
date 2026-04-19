# src/ports/event_consumer_port.py

from abc import ABC, abstractmethod


class EventConsumerPort(ABC):

    @abstractmethod
    def start_consuming(self):
        pass