from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

# Placeholder for saved connections or analytics metadata
connections = Table(
    "connections",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(128)),
)
