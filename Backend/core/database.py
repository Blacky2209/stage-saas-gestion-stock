from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 1. On charge les variables du fichier .env
load_dotenv()

# 2. On récupère l'URL de connexion
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 3. On crée le "Moteur" (Engine)
# C'est lui qui gère la connexion réelle avec PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 4. On crée la "Session"
# Chaque fois qu'on fera une requête, on ouvrira une session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. On crée la "Base"
# Toutes tes futures tables (Models) hériteront de cette classe
Base = declarative_base()

# Fonction utilitaire pour récupérer la BDD dans les routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()