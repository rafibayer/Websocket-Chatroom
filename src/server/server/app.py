from server import Server
from chatroom import Chatroom
from utils import log, log_message
from config_manager import ConfigManager
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s : %(levelname)s : %(name)s : %(message)s')
logger = logging.getLogger(__name__)


class App:
    """
    Main entrypoint for chatroom server, instantiates and runs server
    """

    def __init__(self, server):
        """Create a new app to run a given server

        Args:
            server (Server): app server
        """
        self.server = server

    @log(logger, logging.INFO)
    def start(self):
        """
        Start the server
        """
        self.server.start()


if __name__ == "__main__":
    chatroom_handler = Chatroom("../config/chat.yaml")
    server = Server("../config/server.yaml", chatroom_handler)
    app = App(server)
    app.start()
