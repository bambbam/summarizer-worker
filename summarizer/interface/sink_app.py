import time
from summarizer.interface.container import Container
from summarizer.interface.settings import Settings
from summarizer.interface import handler
class SinkApp:
    def __init__(self, settings: Settings):
        cont = Container()
        cont.config.from_pydantic(settings)
        cont.wire(packages=[handler])
        self.event_listener = cont.event_listener()
        
    def run(self):
        while(True):
            self.run_once()

    def run_once(self):
        incoming = self.event_listener.get()
        print(incoming)
        if incoming is None:
            print("no incomming")
            time.sleep(1)
            return
        handler.handle_message(incoming)