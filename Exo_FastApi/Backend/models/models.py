from sqlalchemy import Column, Integer, String, Date, DateTime 
from sqlalchemy.sql import func
from core.database import Base

class User(Base):
    # Le nom exact de ta table dans la BDD
    __tablename__ = "users" 

    # 1. ID
    id = Column(Integer, primary_key=True, index=True)
    
    # 2. Name (varchar 50)
    name = Column(String(50), nullable=False)
    
    # 3. Firstname (varchar 50, Non Null)
    firstname = Column(String(50), nullable=False)
    
    # 4. Birthday (Date, Non Null)
    # Note : On importe 'Date' (juste jour/mois/année) et pas 'DateTime'
    birthday = Column(Date, nullable=False)
    
    # 5. Date_creation (datetime, default current_timestamp)
    # Attention à bien reprendre le nom exact de ta colonne SQL
    date_creation = Column(DateTime, server_default=func.now(), nullable=False)
    
    # 6. Date_modif (datetime, default current_timestamp)
    # 'onupdate=func.now()' permet de mettre à jour cette date automatiquement quand tu modifies l'user
    date_modif = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


# models/models.py

# ... tes imports et la classe User existante ...

# NOUVELLE CLASSE POUR LA TABLE EVENTS
class Event(Base):
    __tablename__ = "events" # Vérifie que c'est bien le nom dans phpMyAdmin

    id = Column(Integer, primary_key=True, index=True)
    event = Column(String(100), nullable=False)    # Nom de l'event
    city = Column(String(50), nullable=True)  # Ville
    postcode = Column(Integer, nullable=False)           # Code postal de l'event
    date = Column(Date, nullable=False)               # Date de l'event