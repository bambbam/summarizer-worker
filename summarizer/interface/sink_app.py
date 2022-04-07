from summarizer.infrastructure.redis_listener import EventListener
from summarizer.interface.container import Container
from summarizer.interface.settings import Settings

class SinkApp:
    def __init__(self, settings: Settings):
        cont = Container()
        cont.config.from_pydantic(settings)
        
        self.event_listener = cont.event_listener()
    
    def run(self):
        while True:
            self.run_once()
            
    def run_once(self):
        incoming = self.event_listener.get()
        if not incoming:
            return
        for message in incoming:
            ...