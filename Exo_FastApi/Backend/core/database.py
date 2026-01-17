from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ---------------------------------------------------------
# CONFIGURATION XAMPP / MYSQL
# ---------------------------------------------------------
# Syntaxe : mysql+pymysql://user:password@host:port/database_name
# Remplace 'NOM_DE_TA_BASE' par le nom exact dans phpMyAdmin

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/anniversaire"

# Création du moteur (Sans l'argument check_same_thread qui était pour SQLite)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()