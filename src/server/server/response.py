import datetime
import json
from enum import Enum


class Origin(Enum):
    """Response origin Enum
    """
    DEFAULT = "DEFAULT"
    SERVER = "SERVER"
    USER = "USER"
    SELF = "SELF"
    PRIVATE = "PRIVATE"


class Response:

    def __init__(self, body, origin=Origin.DEFAULT):
        """Creates a new response

        Args:
            body (str): response body
            origin (Origin, optional): Origin of body. Defaults to Origin.DEFAULT.
        """
        self.data = {
            "body": str(body),
            "origin": origin.value,
            "sentAt": str(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        }

    def json(self):
        return json.dumps(self.data)

    def __str__(self):
        return self.json()

    def __repr__(self):
        return f"<Response {self.json()}>"
