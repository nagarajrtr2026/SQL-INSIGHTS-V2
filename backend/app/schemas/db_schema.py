from pydantic import BaseModel


class DBConnectSchema(BaseModel):
    kind: str
    host: str
    port: int
    username: str
    password: str
    database: str
from pydantic import BaseModel


class DBConnection(BaseModel):
    kind: str
    host: str
    port: int
    username: str
    password: str
    database: str
