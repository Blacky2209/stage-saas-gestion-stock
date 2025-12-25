from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models import Tenant
from schemas.tenant import TenantCreate, TenantResponse

# On crée le "guichet" pour les tenants
router = APIRouter(
    prefix="/tenants",
    tags=["Entreprises (Tenants)"]
)

# 1. Route pour CRÉER une entreprise (POST)
@router.post("/", response_model=TenantResponse)
def create_tenant(tenant: TenantCreate, db: Session = Depends(get_db)):
    # On prépare la nouvelle ligne à ajouter
    db_tenant = Tenant(nom_societe=tenant.nom_societe, adresse=tenant.adresse)
    
    # On l'ajoute et on valide
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant) # On récupère l'ID généré automatiquement
    
    return db_tenant

# 2. Route pour LIRE toutes les entreprises (GET)
@router.get("/", response_model=list[TenantResponse])
def read_tenants(db: Session = Depends(get_db)):
    return db.query(Tenant).all()