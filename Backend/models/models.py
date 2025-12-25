from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

# 1. Table TENANTS (Entreprises)
class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    nom_societe = Column(String, nullable=False)
    adresse = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Liens
    users = relationship("User", back_populates="tenant")
    produits = relationship("Product", back_populates="tenant")

# 2. Table USERS
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    nom = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    mot_de_passe = Column(String)
    role = Column(String, default="employe")

    tenant = relationship("Tenant", back_populates="users")

# 3. Table PRODUITS
class Product(Base):
    __tablename__ = "produits"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    nom = Column(String, index=True)
    description = Column(Text, nullable=True)
    sku = Column(String, index=True)
    prix = Column(DECIMAL(10, 2))
    quantite_stock = Column(Integer, default=0)
    seuil_alerte = Column(Integer, default=10)

    tenant = relationship("Tenant", back_populates="produits")
    mouvements = relationship("Movement", back_populates="product")

# 4. Table MOUVEMENTS
class Movement(Base):
    __tablename__ = "mouvements"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    product_id = Column(Integer, ForeignKey("produits.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    type_mouvement = Column(String) 
    quantite = Column(Integer)
    motif = Column(String)
    date_mouvement = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="mouvements")