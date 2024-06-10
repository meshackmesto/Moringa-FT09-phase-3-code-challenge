from .setup import create_tables
from .connection import get_db_connection

# Initialize the database and create tables if they don't exist
create_tables()

# You can also choose to import the connection function if you want it to be available
# directly from the package
__all__ = ["get_db_connection", "create_tables"]
