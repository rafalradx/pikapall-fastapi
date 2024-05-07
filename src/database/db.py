from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo_pool=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# db session with automatic closing
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as err:
        # log your error
        print(err)  # for dev/testing
        db.rollback()
    finally:
        db.close()
