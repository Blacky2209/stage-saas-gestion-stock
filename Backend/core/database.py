from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Configuration de la base de données (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 2. LA FONCTION ESSENTIELLE (C'est celle qui manquait !) ⬇️
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()