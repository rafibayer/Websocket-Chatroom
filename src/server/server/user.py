import datetime
from uuid import uuid4


class User:
    """
    Stores user data for connected websocket client
    """

    def __init__(self, websocket, name):
        """
        Creates a new user for a given websocket and name

        Args:
            websocket (Websocket): User websocket connection
            name (str): Users name
        """
        self.websocket = websocket
        self.name = name
        self.connected_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.uuid = str(uuid4())

    def __repr__(self):
        """
        returns str representation of User including name, connection datetime, and status

        Returns:
            str: str representation of User
        """
        conn_str = "Connected" if self.websocket.open else "Disconnected"
        return f"<{self.name=},{self.connected_at=}, Status: {conn_str}, {self.uuid=}>"
