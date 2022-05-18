from summarizer.interface.settings import Settings
from summarizer.interface.sink_app import SinkApp

def main():
    app = SinkApp(Settings())
    app.run()

if __name__=="__main__":
    main()
