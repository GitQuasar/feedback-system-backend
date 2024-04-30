from enum import Enum

class Status(str, Enum):
    Created = "Created"
    Replied = "Replied"

class Role(str, Enum):
    Admin = "Administrator"
    Manager = "Manager"