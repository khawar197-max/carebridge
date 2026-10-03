from database.database import Base, engine
from database import models


def init_database():
    """
    Create all CareBridge database tables if they do not already exist.
    Safe to run every time the Streamlit app starts.
    """
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_database()
    print("CareBridge database initialized successfully.")
