from database.database import Base, engine
from database import models


def init_database():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_database()
    print("CareBridge database initialized successfully.")
