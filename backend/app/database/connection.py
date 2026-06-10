from sqlalchemy import create_engine
from urllib.parse import quote_plus


def build_db_url(kind: str, host: str, port: int, user: str, password: str, db: str) -> str:
    if kind == "postgresql":
        return f"postgresql://{user}:{quote_plus(password)}@{host}:{port}/{db}"
    elif kind == "mysql":
        return f"mysql+pymysql://{user}:{quote_plus(password)}@{host}:{port}/{db}"
    else:
        raise ValueError("Unsupported DB kind")


def create_sync_engine(db_url: str):
    return create_engine(db_url, pool_pre_ping=True)
